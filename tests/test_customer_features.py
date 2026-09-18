import pandas as pd
import pytest

from src.customer_features import (
    create_customer_features,
    validate_customer_features,
)


def test_customer_features_create_one_row_per_order(
    customers_df,
    orders_df,
):
    """Customer feature output must contain one row per order."""
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    assert len(customer_features_df) == len(orders_df)
    assert customer_features_df["order_id"].nunique() == len(
        orders_df
    )
    assert not customer_features_df["order_id"].duplicated().any()


def test_first_order_has_no_prior_history(
    customers_df,
    orders_df,
):
    """A customer's first order should have zero prior history."""
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    first_order = customer_features_df[
        customer_features_df["order_id"] == "ORD-001"
    ].iloc[0]

    assert first_order["customer_id"] == "CUST-001"
    assert first_order["prior_order_count"] == 0
    assert first_order["prior_total_spend"] == 0
    assert first_order["prior_return_count"] == 0
    assert first_order["is_first_order"] == 1
    assert pd.isna(first_order["prior_return_rate"])


def test_second_order_uses_only_prior_customer_history(
    customers_df,
    orders_df,
):
    """
    The second order must use the first order as history,
    but must not include its own outcome or spend.
    """
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    second_order = customer_features_df[
        customer_features_df["order_id"] == "ORD-002"
    ].iloc[0]

    assert second_order["customer_id"] == "CUST-001"
    assert second_order["prior_order_count"] == 1
    assert second_order["prior_total_spend"] == 100.0
    assert second_order["prior_total_discount"] == 10.0
    assert second_order["prior_return_count"] == 0
    assert second_order["prior_return_rate"] == 0.0
    assert second_order["is_first_order"] == 0

    # 31 days and 1 hour between ORD-001 and ORD-002.
    assert second_order["days_since_previous_order"] == pytest.approx(
        31 + (1 / 24)
    )


def test_customer_static_attributes_are_merged(
    customers_df,
    orders_df,
):
    """Customer attributes should be attached to every order."""
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    order_row = customer_features_df[
        customer_features_df["order_id"] == "ORD-004"
    ].iloc[0]

    assert order_row["customer_age"] == 40
    assert order_row["gender"] == "Male"
    assert order_row["customer_segment"] == "Corporate"
    assert order_row["customer_state"] == "Texas"
    assert order_row["region"] == "South"


def test_customer_feature_output_has_no_target_column(
    customers_df,
    orders_df,
):
    """Customer feature output must not include the ML target."""
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    assert "return_label" not in customer_features_df.columns


def test_customer_features_reject_invalid_timestamp(
    customers_df,
    orders_df,
):
    """Invalid order date/time values should stop feature creation."""
    invalid_orders_df = orders_df.copy()

    invalid_orders_df.loc[
        invalid_orders_df["order_id"] == "ORD-001",
        "order_date",
    ] = "not-a-valid-date"

    with pytest.raises(
        ValueError,
        match="Invalid order date/time values found",
    ):
        create_customer_features(
            customers_df=customers_df,
            orders_df=invalid_orders_df,
        )


def test_validate_customer_features_rejects_duplicate_orders(
    customers_df,
    orders_df,
):
    """Validation should reject duplicate order IDs."""
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    invalid_features_df = pd.concat(
        [
            customer_features_df,
            customer_features_df.iloc[[0]],
        ],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="row count does not match|Duplicate order IDs",
    ):
        validate_customer_features(
            customer_features_df=invalid_features_df,
            expected_order_count=len(orders_df),
        )