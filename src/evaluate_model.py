from datetime import datetime, timezone
import json

import joblib
import numpy as np
import pandas as pd

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from src.build_training_data import (
    TRAINING_DATA_FILE,
    get_model_feature_columns,
)
from src.config import (
    MODELS_DIR,
    MODEL_VERSION,
    ORDER_TIMESTAMP_COLUMN,
    RANDOM_SEED,
    TARGET_COLUMN,
    TEST_END_DATE,
    TEST_START_DATE,
    VALIDATION_END_DATE,
)
from src.train_models import (
    MODEL_RESULTS_FILE,
    create_linear_preprocessor,
    create_tree_preprocessor,
    get_column_types,
    prepare_catboost_data,
)


MODEL_FILE = MODELS_DIR / f"{MODEL_VERSION}.joblib"
METADATA_FILE = MODELS_DIR / f"{MODEL_VERSION}_metadata.json"
TEST_METRICS_FILE = MODELS_DIR / f"{MODEL_VERSION}_test_metrics.csv"
FEATURE_IMPORTANCE_FILE = (
    MODELS_DIR / f"{MODEL_VERSION}_feature_importance.csv"
)


def select_best_model(
    validation_results_df: pd.DataFrame,
) -> pd.Series:
    """Select the model with the highest validation PR-AUC."""
    required_columns = [
        "model",
        "pr_auc",
        "roc_auc",
        "best_threshold",
        "precision",
        "recall",
        "f1_score",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in validation_results_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Validation results missing columns: {missing_columns}"
        )

    ranked_results_df = (
        validation_results_df
        .sort_values(
            ["pr_auc", "f1_score", "roc_auc"],
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return ranked_results_df.iloc[0]


def split_final_training_and_test_data(
    training_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create final training and untouched test datasets.

    Final training uses data through June 2025.
    Test uses July through December 2025.
    """
    data = training_df.copy()

    data[ORDER_TIMESTAMP_COLUMN] = pd.to_datetime(
        data[ORDER_TIMESTAMP_COLUMN],
        errors="coerce",
    )

    if data[ORDER_TIMESTAMP_COLUMN].isna().any():
        raise ValueError("Invalid order timestamps found.")

    final_training_df = data[
        data[ORDER_TIMESTAMP_COLUMN]
        <= pd.Timestamp(VALIDATION_END_DATE)
    ].copy()

    test_df = data[
        (data[ORDER_TIMESTAMP_COLUMN]
         >= pd.Timestamp(TEST_START_DATE))
        & (
            data[ORDER_TIMESTAMP_COLUMN]
            <= pd.Timestamp(TEST_END_DATE)
        )
    ].copy()

    if final_training_df.empty or test_df.empty:
        raise ValueError(
            "Final training or test dataset is empty."
        )

    return final_training_df, test_df


def create_selected_model(
    model_name: str,
    numeric_columns: list[str],
    categorical_columns: list[str],
    positive_class_weight: float,
):
    """Create the selected model using its final configuration."""
    if model_name == "Logistic Regression":
        return Pipeline([
            (
                "preprocessor",
                create_linear_preprocessor(
                    numeric_columns,
                    categorical_columns,
                ),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    solver="saga",
                    random_state=RANDOM_SEED,
                ),
            ),
        ])

    if model_name == "LightGBM":
        return Pipeline([
            (
                "preprocessor",
                create_tree_preprocessor(
                    numeric_columns,
                    categorical_columns,
                ),
            ),
            (
                "model",
                LGBMClassifier(
                    objective="binary",
                    n_estimators=500,
                    learning_rate=0.03,
                    num_leaves=31,
                    min_child_samples=50,
                    subsample=0.8,
                    subsample_freq=1,
                    colsample_bytree=0.8,
                    reg_lambda=1.0,
                    scale_pos_weight=positive_class_weight,
                    random_state=RANDOM_SEED,
                    n_jobs=-1,
                    verbosity=-1,
                ),
            ),
        ])

    if model_name == "XGBoost":
        return Pipeline([
            (
                "preprocessor",
                create_tree_preprocessor(
                    numeric_columns,
                    categorical_columns,
                ),
            ),
            (
                "model",
                XGBClassifier(
                    n_estimators=400,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    min_child_weight=5,
                    reg_lambda=1.0,
                    scale_pos_weight=positive_class_weight,
                    objective="binary:logistic",
                    eval_metric="aucpr",
                    tree_method="hist",
                    random_state=RANDOM_SEED,
                    n_jobs=-1,
                ),
            ),
        ])

    if model_name == "CatBoost":
        return CatBoostClassifier(
            iterations=500,
            depth=7,
            learning_rate=0.05,
            loss_function="Logloss",
            eval_metric="PRAUC",
            class_weights=[
                1.0,
                positive_class_weight,
            ],
            random_seed=RANDOM_SEED,
            verbose=False,
            allow_writing_files=False,
        )

    raise ValueError(
        f"Unsupported selected model: {model_name}"
    )


def create_feature_importance(
    model,
    model_name: str,
    feature_columns: list[str],
) -> pd.DataFrame:
    """Create a feature-importance table for the saved model."""
    if model_name in ["LightGBM", "XGBoost"]:
        feature_names = (
            model.named_steps["preprocessor"]
            .get_feature_names_out()
        )
        importance_values = (
            model.named_steps["model"]
            .feature_importances_
        )

    elif model_name == "Logistic Regression":
        feature_names = (
            model.named_steps["preprocessor"]
            .get_feature_names_out()
        )
        importance_values = np.abs(
            model.named_steps["model"].coef_[0]
        )

    elif model_name == "CatBoost":
        feature_names = feature_columns
        importance_values = model.feature_importances_

    else:
        raise ValueError(
            f"Feature importance unsupported for: {model_name}"
        )

    return (
        pd.DataFrame({
            "feature": feature_names,
            "importance": importance_values,
        })
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )


def train_evaluate_and_export_model() -> dict:
    """
    Select the best validation model, retrain it, test it once,
    and save the final model artifact and metadata.
    """
    if not TRAINING_DATA_FILE.exists():
        raise FileNotFoundError(
            "Training data not found. "
            "Run build_training_data first."
        )

    if not MODEL_RESULTS_FILE.exists():
        raise FileNotFoundError(
            "Validation model results not found. "
            "Run train_models first."
        )

    training_df = pd.read_csv(TRAINING_DATA_FILE)
    validation_results_df = pd.read_csv(MODEL_RESULTS_FILE)

    selected_model_row = select_best_model(
        validation_results_df
    )

    selected_model_name = selected_model_row["model"]
    selected_threshold = float(
        selected_model_row["best_threshold"]
    )

    final_training_df, test_df = (
        split_final_training_and_test_data(training_df)
    )

    feature_columns = get_model_feature_columns(training_df)

    X_final_train = final_training_df[feature_columns].copy()
    y_final_train = final_training_df[TARGET_COLUMN].copy()

    X_test = test_df[feature_columns].copy()
    y_test = test_df[TARGET_COLUMN].copy()

    numeric_columns, categorical_columns = get_column_types(
        X_final_train,
        feature_columns,
    )

    positive_class_weight = (
        (y_final_train == 0).sum()
        / (y_final_train == 1).sum()
    )

    final_model = create_selected_model(
        model_name=selected_model_name,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        positive_class_weight=positive_class_weight,
    )

    if selected_model_name == "CatBoost":
        X_final_train_model = prepare_catboost_data(
            X_final_train,
            categorical_columns,
        )

        X_test_model = prepare_catboost_data(
            X_test,
            categorical_columns,
        )

        final_model.fit(
            X_final_train_model,
            y_final_train,
            cat_features=categorical_columns,
        )

    else:
        X_final_train_model = X_final_train
        X_test_model = X_test

        final_model.fit(
            X_final_train_model,
            y_final_train,
        )

    test_probabilities = final_model.predict_proba(
        X_test_model
    )[:, 1]

    test_predictions = (
        test_probabilities >= selected_threshold
    ).astype(int)

    test_metrics = {
        "model": selected_model_name,
        "decision_threshold": selected_threshold,
        "test_pr_auc": average_precision_score(
            y_test,
            test_probabilities,
        ),
        "test_roc_auc": roc_auc_score(
            y_test,
            test_probabilities,
        ),
        "test_precision": precision_score(
            y_test,
            test_predictions,
            zero_division=0,
        ),
        "test_recall": recall_score(
            y_test,
            test_predictions,
            zero_division=0,
        ),
        "test_f1_score": f1_score(
            y_test,
            test_predictions,
            zero_division=0,
        ),
        "test_accuracy": accuracy_score(
            y_test,
            test_predictions,
        ),
        "test_return_rate": y_test.mean(),
    }

    model_artifact = {
        "model": final_model,
        "model_name": selected_model_name,
        "model_version": MODEL_VERSION,
        "decision_threshold": selected_threshold,
        "feature_columns": feature_columns,
        "categorical_columns": categorical_columns,
    }

    metadata = {
        "model_version": MODEL_VERSION,
        "model_name": selected_model_name,
        "decision_threshold": selected_threshold,
        "primary_selection_metric": "validation_pr_auc",
        "validation_selection_results": {
            key: (
                float(value)
                if isinstance(value, (float, np.floating))
                else value
            )
            for key, value in selected_model_row.to_dict().items()
        },
        "test_metrics": {
            key: (
                float(value)
                if isinstance(value, (float, np.floating))
                else value
            )
            for key, value in test_metrics.items()
        },
        "feature_columns": feature_columns,
        "categorical_columns": categorical_columns,
        "training_period": {
            "start": str(
                final_training_df[
                    ORDER_TIMESTAMP_COLUMN
                ].min()
            ),
            "end": str(
                final_training_df[
                    ORDER_TIMESTAMP_COLUMN
                ].max()
            ),
            "rows": int(len(final_training_df)),
        },
        "test_period": {
            "start": str(
                test_df[ORDER_TIMESTAMP_COLUMN].min()
            ),
            "end": str(
                test_df[ORDER_TIMESTAMP_COLUMN].max()
            ),
            "rows": int(len(test_df)),
        },
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model_artifact, MODEL_FILE)

    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)

    pd.DataFrame([test_metrics]).to_csv(
        TEST_METRICS_FILE,
        index=False,
    )

    feature_importance_df = create_feature_importance(
        model=final_model,
        model_name=selected_model_name,
        feature_columns=feature_columns,
    )

    feature_importance_df.to_csv(
        FEATURE_IMPORTANCE_FILE,
        index=False,
    )

    print(f"Selected model: {selected_model_name}")
    print(f"Decision threshold: {selected_threshold:.2f}")
    print("\nTest metrics:")
    print(pd.DataFrame([test_metrics]).to_string(index=False))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            test_predictions,
            target_names=["Not Returned", "Returned"],
            zero_division=0,
        )
    )

    print(f"\nSaved model: {MODEL_FILE}")
    print(f"Saved metadata: {METADATA_FILE}")

    return {
        "model": final_model,
        "model_name": selected_model_name,
        "test_metrics": test_metrics,
        "feature_importance": feature_importance_df,
    }


if __name__ == "__main__":
    train_evaluate_and_export_model()