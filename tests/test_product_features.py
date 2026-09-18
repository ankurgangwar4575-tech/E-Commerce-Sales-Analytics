import pandas as pd
import pytest

from src.product_features import (
    create_product_features,
    validate_product_features,
)


def test_product_features_create_one_row_per_order(
    order_items_df,
    products_df,
):
    """Product feature output must contain one row per unique order."""
    product_features_df = create_product_features(
        order_items_df=order_items_df,
        products_df=products_df,
    )

    assert len(product_features_df) == (
        order_items_df["order_id"].nunique()
    )

    assert product_features_df["order_id"].nunique() == 4
    assert not product_features_df["order_id"].duplicated().any()


def test_product_features_aggregate_order_items(
    order_items_df,
    products_df,
):
    """Multiple item rows should aggregate correctly into one order."""
    product_features_df = create_product_features(
        order_items_df=order_items_df,
        products_df=products_df,
    )

    order_one = product_features_df[
        product_features_df["order_id"] == "ORD-001"
    ].iloc[0]

    assert order_one["item_count"] == 2
    assert order_one["unique_product_count"] == 2
    assert order_one["total_quantity"] == 3
    assert order_one["category_count"] == 2
    assert order_one["brand_count"] == 2

    assert order_one["total_gross_sales"] == 200.0
    assert order_one["total_discount_amount"] == 10.0
    assert order_one["total_item_net_sales"] == 210.0
    assert order_one["total_item_profit"] == 100.0


def test_product_features_calculate_rates_correctly(
    order_items_df,
    products_df,
):
    """Discount rate and profit margin should use aggregated values."""
    product_features_df = create_product_features(
        order_items_df=order_items_df,
        products_df=products_df,
    )

    order_one = product_features_df[
        product_features_df["order_id"] == "ORD-001"
    ].iloc[0]

    assert order_one["order_discount_rate"] == pytest.approx(5.0)

    expected_margin = (100.0 / 210.0) * 100

    assert order_one[
        "order_profit_margin_percentage"
    ] == pytest.approx(expected_margin)


def test_product_features_select_dominant_category(
    order_items_df,
    products_df,
):
    """
    When category sales are tied, alphabetical category order
    should choose the dominant category deterministically.
    """
    product_features_df = create_product_features(
        order_items_df=order_items_df,
        products_df=products_df,
    )

    order_one = product_features_df[
        product_features_df["order_id"] == "ORD-001"
    ].iloc[0]

    assert order_one["dominant_product_category"] == "Electronics"


def test_product_features_reject_missing_catalog_product(
    order_items_df,
    products_df,
):
    """An item without a matching catalog product must fail."""
    invalid_order_items_df = order_items_df.copy()

    invalid_order_items_df.loc[
        invalid_order_items_df["order_id"] == "ORD-001",
        "product_id",
    ] = "PROD-UNKNOWN"

    with pytest.raises(
        ValueError,
        match="do not match a product catalog record",
    ):
        create_product_features(
            order_items_df=invalid_order_items_df,
            products_df=products_df,
        )


def test_product_features_reject_duplicate_catalog_product(
    order_items_df,
    products_df,
):
    """Duplicate product IDs in the catalog must fail."""
    invalid_products_df = pd.concat(
        [
            products_df,
            products_df.iloc[[0]],
        ],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="Duplicate product IDs",
    ):
        create_product_features(
            order_items_df=order_items_df,
            products_df=invalid_products_df,
        )


def test_validate_product_features_rejects_duplicate_orders(
    order_items_df,
    products_df,
):
    """Validation should reject duplicate order IDs."""
    product_features_df = create_product_features(
        order_items_df=order_items_df,
        products_df=products_df,
    )

    invalid_features_df = pd.concat(
        [
            product_features_df,
            product_features_df.iloc[[0]],
        ],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="row count does not match|Duplicate order IDs",
    ):
        validate_product_features(
            product_features_df=invalid_features_df,
            expected_order_count=4,
        )