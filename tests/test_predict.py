import numpy as np
import pandas as pd
import pytest

from src.predict import (
    assign_risk_level,
    predict_return_risk,
    validate_prediction_input,
)


class FakeProbabilityModel:
    """
    Small fake model used only for testing prediction logic.
    """

    def predict_proba(self, dataframe):
        probabilities = dataframe["mock_probability"].to_numpy()

        return np.column_stack([
            1 - probabilities,
            probabilities,
        ])


@pytest.fixture
def fake_model_artifact():
    return {
        "model": FakeProbabilityModel(),
        "model_name": "Fake Test Model",
        "model_version": "test_v1",
        "decision_threshold": 0.70,
        "feature_columns": [
            "mock_probability",
            "customer_segment",
        ],
        "categorical_columns": [
            "customer_segment",
        ],
    }


def test_assign_risk_level():
    """Risk labels should follow the configured threshold."""
    assert assign_risk_level(0.80, 0.70) == "High"
    assert assign_risk_level(0.50, 0.70) == "Medium"
    assert assign_risk_level(0.10, 0.70) == "Low"


def test_prediction_returns_probability_and_risk_level(
    fake_model_artifact,
):
    """Prediction output should contain probability, class, and risk."""
    input_df = pd.DataFrame({
        "mock_probability": [0.80, 0.50, 0.10],
        "customer_segment": [
            "Consumer",
            "Corporate",
            "Consumer",
        ],
    })

    prediction_df = predict_return_risk(
        input_dataframe=input_df,
        model_artifact=fake_model_artifact,
    )

    assert list(prediction_df.columns) == [
        "return_probability",
        "predicted_return",
        "risk_level",
    ]

    assert prediction_df["return_probability"].tolist() == [
        0.80,
        0.50,
        0.10,
    ]

    assert prediction_df["predicted_return"].tolist() == [
        1,
        0,
        0,
    ]

    assert prediction_df["risk_level"].tolist() == [
        "High",
        "Medium",
        "Low",
    ]


def test_prediction_rejects_missing_features(
    fake_model_artifact,
):
    """Prediction should fail when required model input is absent."""
    input_df = pd.DataFrame({
        "customer_segment": ["Consumer"],
    })

    with pytest.raises(
        ValueError,
        match="missing required features",
    ):
        predict_return_risk(
            input_dataframe=input_df,
            model_artifact=fake_model_artifact,
        )


def test_validate_prediction_input_rejects_empty_dataframe():
    """Prediction input cannot be empty."""
    empty_input_df = pd.DataFrame({
        "mock_probability": [],
        "customer_segment": [],
    })

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        validate_prediction_input(
            input_dataframe=empty_input_df,
            required_features=[
                "mock_probability",
                "customer_segment",
            ],
        )


def test_prediction_fills_missing_category(
    fake_model_artifact,
):
    """Missing categorical values should become Unknown safely."""
    input_df = pd.DataFrame({
        "mock_probability": [0.80],
        "customer_segment": [None],
    })

    prediction_df = predict_return_risk(
        input_dataframe=input_df,
        model_artifact=fake_model_artifact,
    )

    assert prediction_df["risk_level"].iloc[0] == "High"