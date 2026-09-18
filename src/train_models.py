import numpy as np
import pandas as pd

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    MinMaxScaler,
    OneHotEncoder,
    StandardScaler,
)
from xgboost import XGBClassifier

from src.build_training_data import (
    TRAINING_DATA_FILE,
    get_model_feature_columns,
)
from src.config import (
    ORDER_TIMESTAMP_COLUMN,
    RANDOM_SEED,
    TARGET_COLUMN,
    TEST_END_DATE,
    TEST_START_DATE,
    TRAIN_END_DATE,
    VALIDATION_END_DATE,
    VALIDATION_START_DATE,
)


MODEL_RESULTS_FILE = (
    TRAINING_DATA_FILE.parent
    / "model_validation_results.csv"
)


def split_data_chronologically(
    training_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split data into train, validation, and untouched test periods."""
    data = training_df.copy()

    data[ORDER_TIMESTAMP_COLUMN] = pd.to_datetime(
        data[ORDER_TIMESTAMP_COLUMN],
        errors="coerce",
    )

    if data[ORDER_TIMESTAMP_COLUMN].isna().any():
        raise ValueError("Invalid order timestamps found.")

    train_df = data[
        data[ORDER_TIMESTAMP_COLUMN]
        <= pd.Timestamp(TRAIN_END_DATE)
    ].copy()

    validation_df = data[
        (data[ORDER_TIMESTAMP_COLUMN]
         >= pd.Timestamp(VALIDATION_START_DATE))
        & (
            data[ORDER_TIMESTAMP_COLUMN]
            <= pd.Timestamp(VALIDATION_END_DATE)
        )
    ].copy()

    test_df = data[
        (data[ORDER_TIMESTAMP_COLUMN]
         >= pd.Timestamp(TEST_START_DATE))
        & (
            data[ORDER_TIMESTAMP_COLUMN]
            <= pd.Timestamp(TEST_END_DATE)
        )
    ].copy()

    if train_df.empty or validation_df.empty or test_df.empty:
        raise ValueError(
            "One or more chronological data splits are empty."
        )

    return train_df, validation_df, test_df


def get_column_types(
    dataframe: pd.DataFrame,
    feature_columns: list[str],
) -> tuple[list[str], list[str]]:
    """Separate feature columns into numeric and categorical lists."""
    categorical_columns = dataframe[
        feature_columns
    ].select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    numeric_columns = [
        column
        for column in feature_columns
        if column not in categorical_columns
    ]

    return numeric_columns, categorical_columns


def create_linear_preprocessor(
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> ColumnTransformer:
    """Preprocessing for Logistic Regression."""
    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline([
                    (
                        "imputer",
                        SimpleImputer(strategy="median"),
                    ),
                    (
                        "scaler",
                        StandardScaler(with_mean=False),
                    ),
                ]),
                numeric_columns,
            ),
            (
                "categorical",
                Pipeline([
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="constant",
                            fill_value="Unknown",
                        ),
                    ),
                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore",
                        ),
                    ),
                ]),
                categorical_columns,
            ),
        ]
    )



def create_tree_preprocessor(
    numeric_columns: list[str],
    categorical_columns: list[str],
) -> ColumnTransformer:
    """Preprocessing for Random Forest, XGBoost, and LightGBM."""
    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline([
                    (
                        "imputer",
                        SimpleImputer(strategy="median"),
                    ),
                ]),
                numeric_columns,
            ),
            (
                "categorical",
                Pipeline([
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="constant",
                            fill_value="Unknown",
                        ),
                    ),
                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore",
                        ),
                    ),
                ]),
                categorical_columns,
            ),
        ]
    )


def prepare_catboost_data(
    dataframe: pd.DataFrame,
    categorical_columns: list[str],
) -> pd.DataFrame:
    """Prepare categories and missing values for CatBoost."""
    prepared_df = dataframe.copy()

    prepared_df = prepared_df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    for column in categorical_columns:
        prepared_df[column] = (
            prepared_df[column]
            .fillna("Unknown")
            .astype(str)
        )

    return prepared_df


def find_best_threshold(
    actual_values: pd.Series,
    probabilities: np.ndarray,
) -> tuple[float, pd.DataFrame]:
    """Find the validation threshold with the highest F1-score."""
    threshold_results = []

    for threshold in np.arange(0.05, 0.96, 0.05):
        predictions = (probabilities >= threshold).astype(int)

        threshold_results.append({
            "threshold": round(float(threshold), 2),
            "precision": precision_score(
                actual_values,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                actual_values,
                predictions,
                zero_division=0,
            ),
            "f1_score": f1_score(
                actual_values,
                predictions,
                zero_division=0,
            ),
        })

    threshold_results_df = pd.DataFrame(threshold_results)

    best_threshold = float(
        threshold_results_df.loc[
            threshold_results_df["f1_score"].idxmax(),
            "threshold",
        ]
    )

    return best_threshold, threshold_results_df


def evaluate_candidate_model(
    model_name: str,
    model,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_validation: pd.DataFrame,
    y_validation: pd.Series,
    catboost_columns: list[str] | None = None,
) -> tuple[dict, pd.DataFrame]:
    """Train one model and evaluate it on validation data."""
    if catboost_columns is None:
        model.fit(X_train, y_train)
    else:
        model.fit(
            X_train,
            y_train,
            cat_features=catboost_columns,
        )

    validation_probabilities = model.predict_proba(
        X_validation
    )[:, 1]

    best_threshold, threshold_results_df = find_best_threshold(
        y_validation,
        validation_probabilities,
    )

    validation_predictions = (
        validation_probabilities >= best_threshold
    ).astype(int)

    result = {
        "model": model_name,
        "pr_auc": average_precision_score(
            y_validation,
            validation_probabilities,
        ),
        "roc_auc": roc_auc_score(
            y_validation,
            validation_probabilities,
        ),
        "best_threshold": best_threshold,
        "precision": precision_score(
            y_validation,
            validation_predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_validation,
            validation_predictions,
            zero_division=0,
        ),
        "f1_score": f1_score(
            y_validation,
            validation_predictions,
            zero_division=0,
        ),
    }

    threshold_results_df.insert(0, "model", model_name)

    return result, threshold_results_df


def train_and_compare_models(
    training_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Train all candidate models and compare validation performance.

    The untouched test data is intentionally not used here.
    """
    train_df, validation_df, _ = split_data_chronologically(
        training_df
    )

    feature_columns = get_model_feature_columns(training_df)

    X_train = train_df[feature_columns].copy()
    y_train = train_df[TARGET_COLUMN].copy()

    X_validation = validation_df[feature_columns].copy()
    y_validation = validation_df[TARGET_COLUMN].copy()

    numeric_columns, categorical_columns = get_column_types(
        X_train,
        feature_columns,
    )

    positive_class_weight = (
        (y_train == 0).sum() / (y_train == 1).sum()
    )

    model_definitions = {
        "Logistic Regression": (
            Pipeline([
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
            ]),
            X_train,
            X_validation,
            None,
        ),
        "LightGBM": (
            Pipeline([
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
            ]),
            X_train,
            X_validation,
            None,
        ),
        "XGBoost": (
            Pipeline([
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
            ]),
            X_train,
            X_validation,
            None,
        ),
        "CatBoost": (
            CatBoostClassifier(
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
            ),
            prepare_catboost_data(
                X_train,
                categorical_columns,
            ),
            prepare_catboost_data(
                X_validation,
                categorical_columns,
            ),
            categorical_columns,
        ),
    }

    model_results = []
    threshold_results = []

    for (
        model_name,
        (
            model,
            model_X_train,
            model_X_validation,
            catboost_columns,
        ),
    ) in model_definitions.items():
        print(f"Training {model_name}...")

        result, model_threshold_results = (
            evaluate_candidate_model(
                model_name=model_name,
                model=model,
                X_train=model_X_train,
                y_train=y_train,
                X_validation=model_X_validation,
                y_validation=y_validation,
                catboost_columns=catboost_columns,
            )
        )

        model_results.append(result)
        threshold_results.append(model_threshold_results)

    results_df = (
        pd.DataFrame(model_results)
        .sort_values(
            ["pr_auc", "f1_score", "roc_auc"],
            ascending=False,
        )
        .reset_index(drop=True)
    )

    thresholds_df = pd.concat(
        threshold_results,
        ignore_index=True,
    )

    return results_df, thresholds_df


def save_validation_results(
    results_df: pd.DataFrame,
    thresholds_df: pd.DataFrame,
) -> None:
    """Save model-comparison results for final evaluation."""
    results_df.to_csv(
        MODEL_RESULTS_FILE,
        index=False,
    )

    threshold_file = (
        MODEL_RESULTS_FILE.parent
        / "model_validation_thresholds.csv"
    )

    thresholds_df.to_csv(
        threshold_file,
        index=False,
    )


if __name__ == "__main__":
    if not TRAINING_DATA_FILE.exists():
        raise FileNotFoundError(
            "Training dataset not found. Run build_training_data first."
        )

    training_data = pd.read_csv(TRAINING_DATA_FILE)

    validation_results, threshold_results = (
        train_and_compare_models(training_data)
    )

    save_validation_results(
        validation_results,
        threshold_results,
    )

    print("\nValidation model comparison:")
    print(validation_results.to_string(index=False))

    print(f"\nSaved results to: {MODEL_RESULTS_FILE}")