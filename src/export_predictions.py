from __future__ import annotations

import json
import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.predict import predict_return_risk


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
PREDICTIONS_DIR = DATA_DIR / "predictions"

ORDERS_FILE = DATA_DIR / "ecommerce_sales_customer_analytics_150k.csv"
CUSTOMERS_FILE = DATA_DIR / "customer_master.csv"
TRAINING_FILE = PROCESSED_DIR / "return_risk_training_data.csv"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_artifact(filename: str) -> dict:
    path = MODELS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    return joblib.load(path)


def load_metadata(filename: str) -> dict:
    path = MODELS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Model metadata not found: {path}")
    return load_json(path)


def save_prediction_file(dataframe: pd.DataFrame, filename: str) -> None:
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PREDICTIONS_DIR / filename
    dataframe.to_csv(output_path, index=False)
    print(f"Saved {len(dataframe):,} rows: {output_path}")


def encode_categorical_columns(
    dataframe: pd.DataFrame,
    features: list[str],
    categorical_features: list[str],
    encoders: dict[str, dict[str, int]],
) -> pd.DataFrame:
    """Apply the LabelEncoder mappings saved with the model."""
    encoded = dataframe[features].copy()

    for column in categorical_features:
        mapping = encoders.get(column, {})
        encoded[column] = (
            encoded[column]
            .fillna("Unknown")
            .astype(str)
            .map(mapping)
            .fillna(0)
            .astype(int)
        )

    return encoded


def safe_probability_name(value: object) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")
    return value.lower() or "unknown"


def add_class_probabilities(
    output: pd.DataFrame,
    probabilities: np.ndarray,
    classes: list[object],
    prefix: str,
) -> pd.DataFrame:
    result = output.copy()
    for index, class_name in enumerate(classes):
        result[f"{prefix}_{safe_probability_name(class_name)}"] = (
            probabilities[:, index]
        )
    return result


def export_return_predictions(
    orders_df: pd.DataFrame,
) -> None:
    artifact = load_artifact("return_risk_v1.joblib")
    training_df = pd.read_csv(TRAINING_FILE)

    prediction_input = training_df[artifact["feature_columns"]].copy()
    predictions = predict_return_risk(
        prediction_input,
        model_artifact=artifact,
    )

    order_context = orders_df[
        [
            "order_id",
            "customer_id",
            "order_date",
            "order_time",
            "order_status",
            "return_status",
            "net_sales",
            "profit",
            "region",
        ]
    ].copy()

    order_context = order_context.rename(
        columns={"return_status": "actual_return_status"}
    )

    output = pd.concat(
        [
            training_df[["order_id"]].reset_index(drop=True),
            predictions.reset_index(drop=True),
        ],
        axis=1,
    ).merge(order_context, on="order_id", how="left", validate="1:1")

    output["actual_return_label"] = (
        output["actual_return_status"] == "Returned"
    ).astype(int)

    save_prediction_file(output, "return_predictions.csv")


def export_customer_segmentation(
    orders_df: pd.DataFrame,
    customers_df: pd.DataFrame,
) -> None:
    artifact = load_artifact("customer_segmentation_v1.joblib")
    metadata = load_metadata("customer_segmentation_v1_metadata.json")
    scaler = joblib.load(MODELS_DIR / "segmentation_scaler.joblib")

    customer_metrics = (
        orders_df
        .groupby("customer_id", as_index=False)
        .agg(
            total_orders=("order_id", "count"),
            total_spend=("net_sales", "sum"),
            total_returns=(
                "return_status",
                lambda values: (values == "Returned").sum(),
            ),
        )
    )

    customer_metrics["return_rate"] = (
        customer_metrics["total_returns"]
        / customer_metrics["total_orders"]
    )

    output = customer_metrics.merge(
        customers_df[
            [
                "customer_id",
                "customer_age",
                "gender",
                "customer_segment",
                "customer_country",
                "region",
                "customer_acquisition_cost",
            ]
        ],
        on="customer_id",
        how="left",
        validate="1:1",
    )

    features = metadata["features"]
    output["cluster_id"] = artifact.predict(
        scaler.transform(output[features])
    ).astype(int)
    output["cluster_profile"] = output["cluster_id"].map(
        {int(key): value for key, value in metadata["cluster_profiles"].items()}
    )

    save_prediction_file(output, "customer_segmentation.csv")


def export_segment_classification(
    orders_df: pd.DataFrame,
) -> None:
    artifact = load_artifact("segment_classifier_v1.joblib")
    metadata = load_metadata("segment_classifier_v1_metadata.json")

    features = metadata["features"]
    categorical_features = metadata["cat_features"]
    inputs = encode_categorical_columns(
        orders_df,
        features,
        categorical_features,
        metadata["label_encoders"],
    )

    probabilities = artifact["model"].predict_proba(inputs)
    classes = metadata["target_classes"]
    output = orders_df[
        ["order_id", "customer_id", "order_date", "customer_segment"]
    ].copy()
    output["predicted_segment"] = [
        classes[index] for index in probabilities.argmax(axis=1)
    ]
    output = add_class_probabilities(
        output, probabilities, classes, "segment_probability"
    )

    save_prediction_file(output, "segment_classification.csv")


def export_loyalty_predictions(
    orders_df: pd.DataFrame,
) -> None:
    artifact = load_artifact("loyalty_predictor_v1.joblib")
    metadata = load_metadata("loyalty_predictor_v1_metadata.json")

    inputs = encode_categorical_columns(
        orders_df,
        metadata["features"],
        metadata["cat_features"],
        metadata["label_encoders"],
    )

    output = orders_df[
        [
            "order_id",
            "customer_id",
            "order_date",
            "customer_segment",
            "payment_method",
            "gross_sales",
            "discount_amount",
            "quantity",
            "loyalty_points_earned",
        ]
    ].copy()

    output["predicted_loyalty_points"] = np.maximum(
        0,
        artifact["model"].predict(inputs),
    )
    output["loyalty_prediction_error"] = (
        output["loyalty_points_earned"]
        - output["predicted_loyalty_points"]
    )

    save_prediction_file(output, "loyalty_point_predictions.csv")


def export_multiclass_predictions(
    orders_df: pd.DataFrame,
    model_filename: str,
    metadata_filename: str,
    output_filename: str,
    target_column: str,
    prediction_column: str,
    probability_prefix: str,
) -> None:
    artifact = load_artifact(model_filename)
    metadata = load_metadata(metadata_filename)

    working = orders_df.copy()
    if target_column == "review_sentiment":
        working["return_status"] = working["return_status"].fillna(
            "Not Returned"
        )

    features = metadata["features"]
    valid_rows = working[features].notna().all(axis=1)
    valid = working.loc[valid_rows].copy()

    inputs = encode_categorical_columns(
        valid,
        features,
        metadata["cat_features"],
        metadata["label_encoders"],
    )

    probabilities = artifact["model"].predict_proba(inputs)
    classes = metadata["target_classes"]

    output = valid[
        [
            "order_id",
            "customer_id",
            "order_date",
            "return_status",
            target_column,
        ]
    ].copy()
    output = output.rename(
        columns={
            "return_status": "actual_return_status",
            target_column: f"actual_{target_column}",
        }
    )
    output["is_returned"] = (
        output["actual_return_status"] == "Returned"
    ).astype(int)
    output[prediction_column] = [
        classes[index] for index in probabilities.argmax(axis=1)
    ]
    output = add_class_probabilities(
        output, probabilities, classes, probability_prefix
    )

    save_prediction_file(output, output_filename)


def export_high_value_predictions(
    orders_df: pd.DataFrame,
    customers_df: pd.DataFrame,
) -> None:
    artifact = load_artifact("high_value_v1.joblib")
    metadata = load_metadata("high_value_v1_metadata.json")

    lifetime_value = (
        orders_df
        .groupby("customer_id", as_index=False)
        .agg(
            total_spend=("net_sales", "sum"),
            total_orders=("order_id", "count"),
        )
    )
    lifetime_value["actual_is_high_value"] = (
        lifetime_value["total_spend"]
        >= metadata["ltv_threshold"]
    ).astype(int)

    dated_orders = orders_df.copy()
    dated_orders["order_date"] = pd.to_datetime(dated_orders["order_date"])
    first_orders = (
        dated_orders
        .sort_values("order_date")
        .groupby("customer_id", as_index=False)
        .first()
        .rename(
            columns={
                "net_sales": "first_order_value",
                "discount_amount": "first_order_discount",
                "quantity": "first_order_quantity",
                "sales_channel": "first_order_channel",
            }
        )
    )

    output = customers_df.merge(
        lifetime_value,
        on="customer_id",
        how="inner",
        validate="1:1",
    ).merge(
        first_orders[
            [
                "customer_id",
                "first_order_value",
                "first_order_discount",
                "first_order_quantity",
                "first_order_channel",
            ]
        ],
        on="customer_id",
        how="left",
        validate="1:1",
    )

    # Keep readable source values in the export. Encode a separate copy only
    # for the model, matching the training script's category-code contract.
    model_input = output.copy()
    for column in metadata["categorical_columns"]:
        model_input[column] = model_input[column].astype("category").cat.codes

    inputs = model_input[metadata["features"]]
    probabilities = artifact["model"].predict_proba(inputs)[:, 1]
    output["high_value_probability"] = probabilities
    output["predicted_is_high_value"] = (
        probabilities >= 0.5
    ).astype(int)

    save_prediction_file(output, "high_value_predictions.csv")


def export_rating_predictions(
    orders_df: pd.DataFrame,
) -> None:
    artifact = load_artifact("rating_prediction_v1.joblib")
    metadata = load_metadata("rating_prediction_v1_metadata.json")

    working = orders_df.copy()
    working["is_late"] = (
        working["delivery_days"]
        > working["estimated_delivery_days"]
    ).astype(int)

    features = metadata["features"]
    valid = working.loc[working[features].notna().all(axis=1)].copy()
    predicted_rating = artifact["model"].predict(valid[features])

    output = valid[
        [
            "order_id",
            "customer_id",
            "order_date",
            "delivery_days",
            "estimated_delivery_days",
            "customer_rating",
        ]
    ].copy()
    output = output.rename(
        columns={"customer_rating": "actual_customer_rating"}
    )
    output["predicted_rating"] = np.clip(
        predicted_rating,
        1.0,
        5.0,
    )
    output["rating_prediction_error"] = (
        output["actual_customer_rating"]
        - output["predicted_rating"]
    )

    save_prediction_file(output, "rating_predictions.csv")


def main() -> None:
    orders_df = pd.read_csv(ORDERS_FILE)
    customers_df = pd.read_csv(CUSTOMERS_FILE)

    print(f"Source orders: {len(orders_df):,}")
    print(f"Source customers: {len(customers_df):,}")

    export_return_predictions(orders_df)
    export_customer_segmentation(orders_df, customers_df)
    export_segment_classification(orders_df)
    export_loyalty_predictions(orders_df)
    export_multiclass_predictions(
        orders_df,
        "return_reason_classifier_v1.joblib",
        "return_reason_classifier_v1_metadata.json",
        "return_reason_predictions.csv",
        "return_reason",
        "predicted_return_reason",
        "reason_probability",
    )
    export_multiclass_predictions(
        orders_df,
        "sentiment_classifier_v1.joblib",
        "sentiment_classifier_v1_metadata.json",
        "review_sentiment_predictions.csv",
        "review_sentiment",
        "predicted_review_sentiment",
        "sentiment_probability",
    )
    export_high_value_predictions(orders_df, customers_df)
    export_rating_predictions(orders_df)

    print("\nPower BI prediction exports completed.")
    print(f"Output directory: {PREDICTIONS_DIR}")
    print("Sales forecasting remains available at models/sales_forecast_v1.json")


if __name__ == "__main__":
    main()
