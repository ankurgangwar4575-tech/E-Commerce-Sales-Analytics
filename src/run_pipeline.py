from src.build_training_data import (
    create_training_data,
    load_engineered_features,
    save_training_data,
)
from src.config import ensure_project_directories
from src.customer_features import (
    create_customer_features,
    save_customer_features,
)
from src.evaluate_model import (
    train_evaluate_and_export_model,
)
from src.load_data import load_raw_datasets
from src.product_features import (
    create_product_features,
    save_product_features,
)
from src.train_models import (
    save_validation_results,
    train_and_compare_models,
)
from src.validate_data import (
    raise_if_data_quality_fails,
    validate_data_quality,
)


def run_full_pipeline() -> None:
    """
    Run the full return-risk ML pipeline.

    Steps:
    1. Load raw data
    2. Validate data quality
    3. Create customer features
    4. Create product features
    5. Build final training dataset
    6. Train and compare candidate models
    7. Select, test, and save the best final model
    """
    ensure_project_directories()

    print("\nSTEP 1: Loading raw datasets")
    raw_datasets = load_raw_datasets()

    print("\nSTEP 2: Validating data quality")
    quality_report_df = validate_data_quality(raw_datasets)
    print(quality_report_df.to_string(index=False))
    raise_if_data_quality_fails(quality_report_df)

    print("\nSTEP 3: Creating customer features")
    customer_features_df = create_customer_features(
        customers_df=raw_datasets["customers"],
        orders_df=raw_datasets["orders"],
    )
    save_customer_features(customer_features_df)
    print(
        "Customer features saved: "
        f"{customer_features_df.shape}"
    )

    print("\nSTEP 4: Creating product features")
    product_features_df = create_product_features(
        order_items_df=raw_datasets["order_items"],
        products_df=raw_datasets["products"],
    )
    save_product_features(product_features_df)
    print(
        "Product features saved: "
        f"{product_features_df.shape}"
    )

    print("\nSTEP 5: Building training dataset")
    customer_features_df, product_features_df = (
        load_engineered_features()
    )

    training_df = create_training_data(
        orders_df=raw_datasets["orders"],
        customer_features_df=customer_features_df,
        product_features_df=product_features_df,
    )

    save_training_data(training_df)

    print(
        "Training dataset saved: "
        f"{training_df.shape}"
    )

    print("\nSTEP 6: Training and comparing models")
    validation_results_df, threshold_results_df = (
        train_and_compare_models(training_df)
    )

    save_validation_results(
        validation_results_df,
        threshold_results_df,
    )

    print("\nValidation results:")
    print(validation_results_df.to_string(index=False))

    print("\nSTEP 7: Final evaluation and model export")
    final_result = train_evaluate_and_export_model()

    print("\nPipeline completed successfully.")
    print(f"Selected model: {final_result['model_name']}")
    print("Test metrics:")
    print(final_result["test_metrics"])


if __name__ == "__main__":
    run_full_pipeline()