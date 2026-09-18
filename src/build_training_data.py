import pandas as pd

from src.config import (
    CUSTOMER_ID_COLUMN,
    ELIGIBLE_ORDER_STATUSES,
    FEATURES_DIR,
    FORBIDDEN_FEATURE_COLUMNS,
    ORDER_ID_COLUMN,
    ORDER_TIMESTAMP_COLUMN,
    PROCESSED_DIR,
    TARGET_COLUMN,
    ensure_project_directories,
)
from src.load_data import load_raw_datasets


CUSTOMER_FEATURE_FILE = FEATURES_DIR / "customer_features.csv"
PRODUCT_FEATURE_FILE = FEATURES_DIR / "product_features.csv"

TRAINING_DATA_FILE = (
    PROCESSED_DIR / "return_risk_training_data.csv"
)

PRODUCT_FEATURES_TO_EXCLUDE = [
    "total_discount_amount",
    "maximum_discount_percentage",
    "average_discount_percentage",
    "order_discount_rate",
]


def load_engineered_features() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load customer and product features created by prior pipeline steps."""
    if not CUSTOMER_FEATURE_FILE.exists():
        raise FileNotFoundError(
            f"Customer feature file not found: {CUSTOMER_FEATURE_FILE}"
        )

    if not PRODUCT_FEATURE_FILE.exists():
        raise FileNotFoundError(
            f"Product feature file not found: {PRODUCT_FEATURE_FILE}"
        )

    customer_features_df = pd.read_csv(CUSTOMER_FEATURE_FILE)
    product_features_df = pd.read_csv(PRODUCT_FEATURE_FILE)

    return customer_features_df, product_features_df


def create_training_data(
    orders_df: pd.DataFrame,
    customer_features_df: pd.DataFrame,
    product_features_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine safe order, customer, and product features.

    Returns one row per eligible order with the return_label target.
    """
    if orders_df[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError("Duplicate order IDs found in orders data.")

    if customer_features_df[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Duplicate order IDs found in customer features."
        )

    if product_features_df[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Duplicate order IDs found in product features."
        )

    orders = orders_df.copy()

    orders[ORDER_TIMESTAMP_COLUMN] = pd.to_datetime(
        orders["order_date"].astype(str)
        + " "
        + orders["order_time"].astype(str),
        errors="coerce",
    )

    if orders[ORDER_TIMESTAMP_COLUMN].isna().any():
        raise ValueError("Invalid order timestamps found.")

    orders[TARGET_COLUMN] = (
        orders["return_status"] == "Returned"
    ).astype(int)

    eligible_orders_df = orders[
        orders["order_status"].isin(ELIGIBLE_ORDER_STATUSES)
    ].copy()

    eligible_orders_df["order_month"] = (
        eligible_orders_df[ORDER_TIMESTAMP_COLUMN].dt.month
    )

    eligible_orders_df["order_day_of_week"] = (
        eligible_orders_df[ORDER_TIMESTAMP_COLUMN].dt.dayofweek
    )

    eligible_orders_df["order_hour"] = (
        eligible_orders_df[ORDER_TIMESTAMP_COLUMN].dt.hour
    )

    eligible_orders_df["order_quarter"] = (
        eligible_orders_df[ORDER_TIMESTAMP_COLUMN].dt.quarter
    )

    safe_order_columns = [
        ORDER_ID_COLUMN,
        CUSTOMER_ID_COLUMN,
        ORDER_TIMESTAMP_COLUMN,
        TARGET_COLUMN,
        "order_month",
        "order_day_of_week",
        "order_hour",
        "order_quarter",
        "sales_channel",
        "payment_method",
        "currency",
        "shipping_method",
        "warehouse",
        "marketing_channel",
        "campaign_name",
        "coupon_code",
    ]

    order_training_df = eligible_orders_df[
        safe_order_columns
    ].copy()

    
    customer_columns_to_drop = [
        column
        for column in ["order_timestamp"]
        if column in customer_features_df.columns
    ]

    customer_features_for_merge_df = customer_features_df.drop(
        columns=customer_columns_to_drop,
    )

    product_features_for_merge_df = product_features_df.drop(
        columns=PRODUCT_FEATURES_TO_EXCLUDE,
        errors="ignore",
    )

    training_df = order_training_df.merge(
        customer_features_for_merge_df,
        on=ORDER_ID_COLUMN,
        how="left",
        validate="one_to_one",
        suffixes=("", "_customer"),
    )

    training_df = training_df.merge(
        product_features_for_merge_df,
        on=ORDER_ID_COLUMN,
        how="left",
        validate="one_to_one",
        suffixes=("", "_product"),
    )

    categorical_columns = training_df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    categorical_columns = [
        column
        for column in categorical_columns
        if column != ORDER_ID_COLUMN
    ]

    training_df[categorical_columns] = (
        training_df[categorical_columns]
        .fillna("Unknown")
        .astype(str)
    )

    validate_training_data(
        training_df,
        expected_order_count=len(eligible_orders_df),
    )

    return training_df


def get_model_feature_columns(
    training_df: pd.DataFrame,
) -> list[str]:
    """
    Return approved model input columns.

    IDs, target, timestamps, and forbidden outcome fields are excluded.
    """
    excluded_columns = set(FORBIDDEN_FEATURE_COLUMNS)

    return [
        column
        for column in training_df.columns
        if column not in excluded_columns
    ]


def validate_training_data(
    training_df: pd.DataFrame,
    expected_order_count: int,
) -> None:
    """Validate the final ML training dataset."""
    if len(training_df) != expected_order_count:
        raise ValueError(
            "Training row count does not match eligible-order count."
        )

    if training_df[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Duplicate order IDs found in training dataset."
        )

    if set(training_df[TARGET_COLUMN].unique()) != {0, 1}:
        raise ValueError(
            "return_label must contain only 0 and 1."
        )

    required_feature_columns = [
        "customer_age",
        "item_count",
        "dominant_product_category",
    ]

    missing_required_features = [
        column
        for column in required_feature_columns
        if column not in training_df.columns
        or training_df[column].isna().any()
    ]

    if missing_required_features:
        raise ValueError(
            "Missing required merged features: "
            f"{missing_required_features}"
        )

    model_feature_columns = get_model_feature_columns(training_df)

    unsafe_features = [
        column
        for column in model_feature_columns
        if column in FORBIDDEN_FEATURE_COLUMNS
    ]

    if unsafe_features:
        raise ValueError(
            f"Leakage columns found in model features: {unsafe_features}"
        )


def save_training_data(training_df: pd.DataFrame) -> None:
    """Save the final model-ready training dataset."""
    ensure_project_directories()

    training_df.to_csv(
        TRAINING_DATA_FILE,
        index=False,
    )


if __name__ == "__main__":
    raw_datasets = load_raw_datasets()

    customer_features, product_features = load_engineered_features()

    training_data = create_training_data(
        orders_df=raw_datasets["orders"],
        customer_features_df=customer_features,
        product_features_df=product_features,
    )

    save_training_data(training_data)

    model_features = get_model_feature_columns(training_data)

    print(
        "Training dataset created successfully: "
        f"{training_data.shape}"
    )
    print(f"Model features: {len(model_features)}")
    print(
        "Return rate: "
        f"{training_data[TARGET_COLUMN].mean() * 100:.2f}%"
    )
    print(f"Saved to: {TRAINING_DATA_FILE}")