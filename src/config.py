from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"
PROCESSED_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
TESTS_DIR = PROJECT_ROOT / "tests"



RANDOM_SEED = 42
MODEL_VERSION = "return_risk_v1"



TARGET_COLUMN = "return_label"
ORDER_ID_COLUMN = "order_id"
CUSTOMER_ID_COLUMN = "customer_id"
ORDER_TIMESTAMP_COLUMN = "order_timestamp"

ELIGIBLE_ORDER_STATUSES = [
    "Completed",
    "Returned",
]



TRAIN_END_DATE = "2024-12-31 23:59:59"

VALIDATION_START_DATE = "2025-01-01 00:00:00"
VALIDATION_END_DATE = "2025-06-30 23:59:59"

TEST_START_DATE = "2025-07-01 00:00:00"
TEST_END_DATE = "2025-12-31 23:59:59"



FORBIDDEN_FEATURE_COLUMNS = [
    "order_id",
    "customer_id",
    "order_timestamp",
    "order_timestamp_customer",
    "return_label",
    "order_status",
    "return_status",
    "return_reason",
    "delivery_days",
    "delivery_status",
    "customer_rating",
    "review_sentiment",
    "customer_review",
    "payment_status",
    "loyalty_points_earned",
    "loyalty_points_redeemed",
    "estimated_delivery_days",
    "total_discount_amount",
    "maximum_discount_percentage",
    "average_discount_percentage",
    "order_discount_rate",
]


def ensure_project_directories():
    """Create required generated-data and model folders if absent."""
    for directory in [FEATURES_DIR, PROCESSED_DIR, MODELS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_project_directories()

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Feature directory: {FEATURES_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")
    print(f"Model directory: {MODELS_DIR}")