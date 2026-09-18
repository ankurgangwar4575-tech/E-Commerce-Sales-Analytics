import pandas as pd
import numpy as np

from src.config import (
    CUSTOMER_ID_COLUMN,
    FEATURES_DIR,
    ORDER_ID_COLUMN,
    ensure_project_directories,
)
from src.load_data import load_raw_datasets


CUSTOMER_FEATURE_FILE = FEATURES_DIR / "customer_features.csv"

STATIC_CUSTOMER_COLUMNS = [
    "customer_id",
    "customer_age",
    "gender",
    "customer_segment",
    "customer_state",
    "customer_country",
    "region",
    "customer_acquisition_cost",
]


def create_customer_features(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create one leakage-safe customer feature row per order.

    Historical features use only orders that occurred before
    the current order timestamp.
    """
    required_order_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "order_time",
        "net_sales",
        "discount_amount",
        "return_status",
    ]

    missing_order_columns = [
        column
        for column in required_order_columns
        if column not in orders_df.columns
    ]

    if missing_order_columns:
        raise ValueError(
            f"Orders data is missing columns: {missing_order_columns}"
        )

    missing_customer_columns = [
        column
        for column in STATIC_CUSTOMER_COLUMNS
        if column not in customers_df.columns
    ]

    if missing_customer_columns:
        raise ValueError(
            "Customer data is missing columns: "
            f"{missing_customer_columns}"
        )

    orders = orders_df.copy()

    orders["order_timestamp"] = pd.to_datetime(
        orders["order_date"].astype(str)
        + " "
        + orders["order_time"].astype(str),
        errors="coerce",
    )

    if orders["order_timestamp"].isna().any():
        raise ValueError(
            "Invalid order date/time values found."
        )

    if orders[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Duplicate order IDs found in orders data."
        )

    orders["net_sales"] = pd.to_numeric(
        orders["net_sales"],
        errors="raise",
    )

    orders["discount_amount"] = pd.to_numeric(
        orders["discount_amount"],
        errors="raise",
    )

    orders["return_label"] = (
        orders["return_status"] == "Returned"
    ).astype(int)

    customer_static_df = customers_df[
        STATIC_CUSTOMER_COLUMNS
    ].copy()

    history_base_df = orders[
        [
            "order_id",
            "customer_id",
            "order_timestamp",
            "net_sales",
            "discount_amount",
            "return_label",
        ]
    ].copy()

    
    timestamp_history_df = (
        history_base_df
        .groupby(
            ["customer_id", "order_timestamp"],
            as_index=False,
        )
        .agg(
            orders_at_timestamp=("order_id", "count"),
            net_sales_at_timestamp=("net_sales", "sum"),
            discount_at_timestamp=("discount_amount", "sum"),
            returns_at_timestamp=("return_label", "sum"),
        )
        .sort_values(["customer_id", "order_timestamp"])
        .reset_index(drop=True)
    )

    customer_groups = timestamp_history_df.groupby(
        "customer_id",
        group_keys=False,
    )

    timestamp_history_df["prior_order_count"] = (
        customer_groups["orders_at_timestamp"]
        .transform(
            lambda series: series.cumsum().shift(fill_value=0)
        )
    )

    timestamp_history_df["prior_total_spend"] = (
        customer_groups["net_sales_at_timestamp"]
        .transform(
            lambda series: series.cumsum().shift(fill_value=0)
        )
    )

    timestamp_history_df["prior_total_discount"] = (
        customer_groups["discount_at_timestamp"]
        .transform(
            lambda series: series.cumsum().shift(fill_value=0)
        )
    )

    timestamp_history_df["prior_return_count"] = (
        customer_groups["returns_at_timestamp"]
        .transform(
            lambda series: series.cumsum().shift(fill_value=0)
        )
    )

    timestamp_history_df["previous_order_timestamp"] = (
        customer_groups["order_timestamp"].shift()
    )

    timestamp_history_df["prior_average_order_value"] = np.where(
        timestamp_history_df["prior_order_count"] > 0,
        timestamp_history_df["prior_total_spend"]
        / timestamp_history_df["prior_order_count"],
        np.nan,
    )

    timestamp_history_df["prior_return_rate"] = np.where(
        timestamp_history_df["prior_order_count"] > 0,
        timestamp_history_df["prior_return_count"]
        / timestamp_history_df["prior_order_count"],
        np.nan,
    )

    timestamp_history_df["prior_average_discount"] = np.where(
        timestamp_history_df["prior_order_count"] > 0,
        timestamp_history_df["prior_total_discount"]
        / timestamp_history_df["prior_order_count"],
        np.nan,
    )

    timestamp_history_df["days_since_previous_order"] = (
        timestamp_history_df["order_timestamp"]
        - timestamp_history_df["previous_order_timestamp"]
    ).dt.total_seconds() / (24 * 60 * 60)

    timestamp_history_df["is_first_order"] = (
        timestamp_history_df["prior_order_count"] == 0
    ).astype(int)

    history_feature_columns = [
        "customer_id",
        "order_timestamp",
        "prior_order_count",
        "prior_total_spend",
        "prior_total_discount",
        "prior_return_count",
        "prior_average_order_value",
        "prior_return_rate",
        "prior_average_discount",
        "days_since_previous_order",
        "is_first_order",
    ]

    customer_features_df = history_base_df[
        ["order_id", "customer_id", "order_timestamp"]
    ].merge(
        timestamp_history_df[history_feature_columns],
        on=["customer_id", "order_timestamp"],
        how="left",
        validate="many_to_one",
    )

    customer_features_df = customer_features_df.merge(
        customer_static_df,
        on=CUSTOMER_ID_COLUMN,
        how="left",
        validate="many_to_one",
    )

    validate_customer_features(
        customer_features_df,
        expected_order_count=len(orders_df),
    )

    return customer_features_df


def validate_customer_features(
    customer_features_df: pd.DataFrame,
    expected_order_count: int,
) -> None:
    """Validate the completed customer feature table."""
    if len(customer_features_df) != expected_order_count:
        raise ValueError(
            "Customer feature row count does not match order count."
        )

    if customer_features_df[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Duplicate order IDs found in customer features."
        )

    if "return_label" in customer_features_df.columns:
        raise ValueError(
            "return_label must not be included in customer features."
        )

    first_order_history_errors = customer_features_df.loc[
        customer_features_df["is_first_order"] == 1,
        "prior_order_count",
    ].gt(0).sum()

    if first_order_history_errors > 0:
        raise ValueError(
            "First orders contain non-zero prior order counts."
        )

    if customer_features_df["customer_age"].isna().any():
        raise ValueError(
            "Some orders have no matching customer attributes."
        )


def save_customer_features(
    customer_features_df: pd.DataFrame,
) -> None:
    """Save the customer feature table."""
    ensure_project_directories()

    customer_features_df.to_csv(
        CUSTOMER_FEATURE_FILE,
        index=False,
    )


if __name__ == "__main__":
    raw_datasets = load_raw_datasets()

    customer_features = create_customer_features(
        customers_df=raw_datasets["customers"],
        orders_df=raw_datasets["orders"],
    )

    save_customer_features(customer_features)

    print(
        "Customer features created successfully: "
        f"{customer_features.shape}"
    )
    print(f"Saved to: {CUSTOMER_FEATURE_FILE}")