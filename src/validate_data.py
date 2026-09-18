import pandas as pd

from src.config import (
    CUSTOMER_ID_COLUMN,
    ORDER_ID_COLUMN,
)
from src.load_data import load_raw_datasets


REQUIRED_COLUMNS = {
    "customers": [
        "customer_id",
        "customer_age",
        "gender",
        "customer_segment",
        "customer_country",
        "region",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_date",
        "order_time",
        "order_status",
        "return_status",
    ],
    "order_items": [
        "order_id",
        "product_id",
        "quantity",
    ],
    "products": [
        "product_id",
        "product_category",
        "brand",
        "product_rating",
    ],
    "statistics": [
        "Total Transactions",
    ],
}


def validate_required_columns(
    datasets: dict[str, pd.DataFrame],
) -> list[dict]:
    """Check whether every dataset has its required columns."""
    results = []

    for dataset_name, expected_columns in REQUIRED_COLUMNS.items():
        dataframe = datasets[dataset_name]

        missing_columns = [
            column
            for column in expected_columns
            if column not in dataframe.columns
        ]

        results.append({
            "check": f"{dataset_name}: required columns",
            "status": "PASS" if not missing_columns else "FAIL",
            "value": len(missing_columns),
            "details": (
                "All required columns are present."
                if not missing_columns
                else f"Missing columns: {missing_columns}"
            ),
        })

    return results


def validate_data_quality(
    datasets: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Run key quality checks for source datasets.

    Returns
    -------
    pd.DataFrame
        A PASS/FAIL report for schemas, identifiers, joins, and dates.
    """
    results = validate_required_columns(datasets)

    if any(result["status"] == "FAIL" for result in results):
        return pd.DataFrame(results)

    customers_df = datasets["customers"]
    orders_df = datasets["orders"].copy()
    order_items_df = datasets["order_items"]
    products_df = datasets["products"]

    orders_df["order_timestamp"] = pd.to_datetime(
        orders_df["order_date"].astype(str)
        + " "
        + orders_df["order_time"].astype(str),
        errors="coerce",
    )

    customer_ids = set(customers_df[CUSTOMER_ID_COLUMN])
    order_customer_ids = set(orders_df[CUSTOMER_ID_COLUMN])

    order_ids = set(orders_df[ORDER_ID_COLUMN])
    item_order_ids = set(order_items_df[ORDER_ID_COLUMN])

    product_ids = set(products_df["product_id"])
    item_product_ids = set(order_items_df["product_id"])

    results.extend([
        {
            "check": "Customer IDs are unique",
            "status": (
                "PASS"
                if customers_df[CUSTOMER_ID_COLUMN].duplicated().sum() == 0
                else "FAIL"
            ),
            "value": customers_df[CUSTOMER_ID_COLUMN].duplicated().sum(),
            "details": "Duplicate customer_id values.",
        },
        {
            "check": "Order IDs are unique",
            "status": (
                "PASS"
                if orders_df[ORDER_ID_COLUMN].duplicated().sum() == 0
                else "FAIL"
            ),
            "value": orders_df[ORDER_ID_COLUMN].duplicated().sum(),
            "details": "Duplicate order_id values.",
        },
        {
            "check": "Product IDs are unique",
            "status": (
                "PASS"
                if products_df["product_id"].duplicated().sum() == 0
                else "FAIL"
            ),
            "value": products_df["product_id"].duplicated().sum(),
            "details": "Duplicate product_id values.",
        },
        {
            "check": "Orders have valid customers",
            "status": (
                "PASS"
                if len(order_customer_ids - customer_ids) == 0
                else "FAIL"
            ),
            "value": len(order_customer_ids - customer_ids),
            "details": "Order customer IDs missing from customer master.",
        },
        {
            "check": "Order items have valid orders",
            "status": (
                "PASS"
                if len(item_order_ids - order_ids) == 0
                else "FAIL"
            ),
            "value": len(item_order_ids - order_ids),
            "details": "Order item order IDs missing from orders table.",
        },
        {
            "check": "Orders have order items",
            "status": (
                "PASS"
                if len(order_ids - item_order_ids) == 0
                else "FAIL"
            ),
            "value": len(order_ids - item_order_ids),
            "details": "Orders without item records.",
        },
        {
            "check": "Order items have valid products",
            "status": (
                "PASS"
                if len(item_product_ids - product_ids) == 0
                else "FAIL"
            ),
            "value": len(item_product_ids - product_ids),
            "details": "Order item product IDs missing from catalog.",
        },
        {
            "check": "Order timestamps are valid",
            "status": (
                "PASS"
                if orders_df["order_timestamp"].isna().sum() == 0
                else "FAIL"
            ),
            "value": orders_df["order_timestamp"].isna().sum(),
            "details": "Invalid or missing order date/time values.",
        },
        {
            "check": "Return label is available",
            "status": (
                "PASS"
                if "Returned" in orders_df["return_status"].dropna().unique()
                else "FAIL"
            ),
            "value": (
                orders_df["return_status"] == "Returned"
            ).sum(),
            "details": "Number of orders labelled Returned.",
        },
    ])

    return pd.DataFrame(results)


def raise_if_data_quality_fails(
    quality_report_df: pd.DataFrame,
) -> None:
    """Stop the pipeline when a critical quality check fails."""
    failed_checks_df = quality_report_df[
        quality_report_df["status"] == "FAIL"
    ]

    if failed_checks_df.empty:
        return

    failed_check_names = "\n- ".join(
        failed_checks_df["check"].tolist()
    )

    raise ValueError(
        "Data quality validation failed:\n- "
        + failed_check_names
    )


if __name__ == "__main__":
    raw_datasets = load_raw_datasets()

    quality_report = validate_data_quality(raw_datasets)

    print(quality_report.to_string(index=False))

    raise_if_data_quality_fails(quality_report)

    print("\nAll data quality checks passed.")