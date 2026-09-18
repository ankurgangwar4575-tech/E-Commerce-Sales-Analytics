import numpy as np
import pandas as pd

from src.config import (
    FEATURES_DIR,
    ORDER_ID_COLUMN,
    ensure_project_directories,
)
from src.load_data import load_raw_datasets


PRODUCT_FEATURE_FILE = FEATURES_DIR / "product_features.csv"

REQUIRED_ORDER_ITEM_COLUMNS = [
    "order_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount_percentage",
    "discount_amount",
    "gross_sales",
    "tax_amount",
    "shipping_cost",
    "net_sales",
    "product_cost",
    "profit",
]

REQUIRED_PRODUCT_COLUMNS = [
    "product_id",
    "product_category",
    "product_subcategory",
    "brand",
    "supplier",
    "product_rating",
]


def create_product_features(
    order_items_df: pd.DataFrame,
    products_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create one product/item feature row per order.

    Each order can have multiple items. This function aggregates
    all item-level information into a single order-level row.
    """
    missing_order_item_columns = [
        column
        for column in REQUIRED_ORDER_ITEM_COLUMNS
        if column not in order_items_df.columns
    ]

    if missing_order_item_columns:
        raise ValueError(
            "Order items data is missing columns: "
            f"{missing_order_item_columns}"
        )

    missing_product_columns = [
        column
        for column in REQUIRED_PRODUCT_COLUMNS
        if column not in products_df.columns
    ]

    if missing_product_columns:
        raise ValueError(
            "Product catalog is missing columns: "
            f"{missing_product_columns}"
        )

    if products_df["product_id"].duplicated().any():
        raise ValueError(
            "Duplicate product IDs found in product catalog."
        )

    product_attributes_df = products_df[
        REQUIRED_PRODUCT_COLUMNS
    ].copy()

    item_product_df = order_items_df.merge(
        product_attributes_df,
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    if item_product_df["product_category"].isna().any():
        raise ValueError(
            "Some order items do not match a product catalog record."
        )

    numeric_columns = [
        "quantity",
        "unit_price",
        "discount_percentage",
        "discount_amount",
        "gross_sales",
        "tax_amount",
        "shipping_cost",
        "net_sales",
        "product_cost",
        "profit",
        "product_rating",
    ]

    for column in numeric_columns:
        item_product_df[column] = pd.to_numeric(
            item_product_df[column],
            errors="raise",
        )

    product_features_df = (
        item_product_df
        .groupby(ORDER_ID_COLUMN, as_index=False)
        .agg(
            item_count=("product_id", "count"),
            unique_product_count=("product_id", "nunique"),
            total_quantity=("quantity", "sum"),
            category_count=("product_category", "nunique"),
            subcategory_count=("product_subcategory", "nunique"),
            brand_count=("brand", "nunique"),
            supplier_count=("supplier", "nunique"),
            total_gross_sales=("gross_sales", "sum"),
            total_discount_amount=("discount_amount", "sum"),
            total_tax_amount=("tax_amount", "sum"),
            total_shipping_cost=("shipping_cost", "sum"),
            total_item_net_sales=("net_sales", "sum"),
            total_item_product_cost=("product_cost", "sum"),
            total_item_profit=("profit", "sum"),
            minimum_item_unit_price=("unit_price", "min"),
            maximum_item_unit_price=("unit_price", "max"),
            average_item_unit_price=("unit_price", "mean"),
            minimum_product_rating=("product_rating", "min"),
            maximum_product_rating=("product_rating", "max"),
            average_product_rating=("product_rating", "mean"),
            maximum_discount_percentage=(
                "discount_percentage",
                "max",
            ),
            average_discount_percentage=(
                "discount_percentage",
                "mean",
            ),
            average_quantity_per_item=("quantity", "mean"),
        )
    )

    product_features_df["order_discount_rate"] = np.where(
        product_features_df["total_gross_sales"] > 0,
        (
            product_features_df["total_discount_amount"]
            / product_features_df["total_gross_sales"]
        ) * 100,
        0.0,
    )

    product_features_df["order_profit_margin_percentage"] = (
        np.where(
            product_features_df["total_item_net_sales"] > 0,
            (
                product_features_df["total_item_profit"]
                / product_features_df["total_item_net_sales"]
            ) * 100,
            0.0,
        )
    )

    category_sales_df = (
        item_product_df
        .groupby(
            [ORDER_ID_COLUMN, "product_category"],
            as_index=False,
        )
        .agg(
            category_gross_sales=("gross_sales", "sum"),
        )
        .sort_values(
            [
                ORDER_ID_COLUMN,
                "category_gross_sales",
                "product_category",
            ],
            ascending=[True, False, True],
        )
    )

    dominant_category_df = (
        category_sales_df
        .drop_duplicates(
            subset=[ORDER_ID_COLUMN],
            keep="first",
        )
        .rename(
            columns={
                "product_category": "dominant_product_category",
            }
        )
        [
            [
                ORDER_ID_COLUMN,
                "dominant_product_category",
            ]
        ]
    )

    product_features_df = product_features_df.merge(
        dominant_category_df,
        on=ORDER_ID_COLUMN,
        how="left",
        validate="one_to_one",
    )

    validate_product_features(
        product_features_df,
        expected_order_count=order_items_df[
            ORDER_ID_COLUMN
        ].nunique(),
    )

    return product_features_df


def validate_product_features(
    product_features_df: pd.DataFrame,
    expected_order_count: int,
) -> None:
    """Validate the completed product feature table."""
    if len(product_features_df) != expected_order_count:
        raise ValueError(
            "Product feature row count does not match unique order count."
        )

    if product_features_df[ORDER_ID_COLUMN].duplicated().any():
        raise ValueError(
            "Duplicate order IDs found in product features."
        )

    if product_features_df["item_count"].isna().any():
        raise ValueError(
            "Missing item counts found in product features."
        )

    if (product_features_df["item_count"] <= 0).any():
        raise ValueError(
            "Orders with zero or negative item counts found."
        )

    if product_features_df[
        "dominant_product_category"
    ].isna().any():
        raise ValueError(
            "Missing dominant product categories found."
        )


def save_product_features(
    product_features_df: pd.DataFrame,
) -> None:
    """Save the product feature table."""
    ensure_project_directories()

    product_features_df.to_csv(
        PRODUCT_FEATURE_FILE,
        index=False,
    )


if __name__ == "__main__":
    raw_datasets = load_raw_datasets()

    product_features = create_product_features(
        order_items_df=raw_datasets["order_items"],
        products_df=raw_datasets["products"],
    )

    save_product_features(product_features)

    print(
        "Product features created successfully: "
        f"{product_features.shape}"
    )
    print(f"Saved to: {PRODUCT_FEATURE_FILE}")