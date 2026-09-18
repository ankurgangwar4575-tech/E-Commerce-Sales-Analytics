import json

import joblib
import numpy as np
import pandas as pd

from src.build_training_data import TRAINING_DATA_FILE
from src.config import MODELS_DIR, MODEL_VERSION


MODEL_FILE = MODELS_DIR / f"{MODEL_VERSION}.joblib"
METADATA_FILE = MODELS_DIR / f"{MODEL_VERSION}_metadata.json"


def load_model_artifact() -> tuple[dict, dict]:
    """
    Load the saved model artifact and matching metadata file.
    """
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Model artifact not found: {MODEL_FILE}"
        )

    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Model metadata not found: {METADATA_FILE}"
        )

    model_artifact = joblib.load(MODEL_FILE)

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        model_metadata = json.load(file)

    if (
        model_artifact["model_name"]
        != model_metadata["model_name"]
    ):
        raise ValueError(
            "Model artifact and metadata model names do not match."
        )

    if (
        model_artifact["feature_columns"]
        != model_metadata["feature_columns"]
    ):
        raise ValueError(
            "Model artifact and metadata feature columns do not match."
        )

    return model_artifact, model_metadata


def assign_risk_level(
    return_probability: float,
    decision_threshold: float,
) -> str:
    """
    Assign Low, Medium, or High return-risk labels.
    """
    if return_probability >= decision_threshold:
        return "High"

    if return_probability >= decision_threshold * 0.5:
        return "Medium"

    return "Low"


def validate_prediction_input(
    input_dataframe: pd.DataFrame,
    required_features: list[str],
) -> None:
    """
    Confirm that all features required by the model are available.
    """
    missing_features = [
        column
        for column in required_features
        if column not in input_dataframe.columns
    ]

    if missing_features:
        raise ValueError(
            "Prediction input is missing required features: "
            f"{missing_features}"
        )

    if input_dataframe.empty:
        raise ValueError(
            "Prediction input cannot be empty."
        )


def predict_return_risk(
    input_dataframe: pd.DataFrame,
    model_artifact: dict | None = None,
) -> pd.DataFrame:
    """
    Predict return probability and risk level.

    Parameters
    ----------
    input_dataframe:
        A DataFrame containing all model-ready input features.
    model_artifact:
        Optional preloaded artifact. If omitted, the saved model
        is loaded automatically.

    Returns
    -------
    pd.DataFrame
        Return probability, predicted class, and risk level.
    """
    if model_artifact is None:
        model_artifact, _ = load_model_artifact()

    model = model_artifact["model"]
    decision_threshold = model_artifact["decision_threshold"]
    required_features = model_artifact["feature_columns"]
    categorical_columns = model_artifact["categorical_columns"]

    validate_prediction_input(
        input_dataframe,
        required_features,
    )

    model_input = (
        input_dataframe[required_features]
        .copy()
        .replace([np.inf, -np.inf], np.nan)
    )

    for column in categorical_columns:
        model_input[column] = (
            model_input[column]
            .fillna("Unknown")
            .astype(str)
        )

    probabilities = model.predict_proba(model_input)[:, 1]

    prediction_results_df = pd.DataFrame({
        "return_probability": probabilities,
    })

    prediction_results_df["predicted_return"] = (
        prediction_results_df["return_probability"]
        >= decision_threshold
    ).astype(int)

    prediction_results_df["risk_level"] = (
        prediction_results_df["return_probability"]
        .apply(
            lambda probability: assign_risk_level(
                probability,
                decision_threshold,
            )
        )
    )

    return prediction_results_df


if __name__ == "__main__":
    if not TRAINING_DATA_FILE.exists():
        raise FileNotFoundError(
            "Training data not found. "
            "Run build_training_data first."
        )

    model_artifact, model_metadata = load_model_artifact()

    training_df = pd.read_csv(TRAINING_DATA_FILE)

    sample_order_df = training_df.sample(
        n=1,
        random_state=42,
    )

    sample_order_id = sample_order_df["order_id"].iloc[0]

    prediction_df = predict_return_risk(
        input_dataframe=sample_order_df,
        model_artifact=model_artifact,
    )

    print(f"Model: {model_metadata['model_name']}")
    print(f"Order ID: {sample_order_id}")
    print(prediction_df.to_string(index=False))