from src.build_training_data import (
    create_training_data,
    get_model_feature_columns,
)
from src.config import FORBIDDEN_FEATURE_COLUMNS
from src.customer_features import create_customer_features
from src.product_features import create_product_features


def create_test_training_data(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Build a small final training dataset from test fixtures."""
    customer_features_df = create_customer_features(
        customers_df=customers_df,
        orders_df=orders_df,
    )

    product_features_df = create_product_features(
        order_items_df=order_items_df,
        products_df=products_df,
    )

    return create_training_data(
        orders_df=orders_df,
        customer_features_df=customer_features_df,
        product_features_df=product_features_df,
    )


def test_training_data_includes_only_eligible_orders(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Pending orders must not enter return-risk training data."""
    training_df = create_test_training_data(
        customers_df,
        orders_df,
        order_items_df,
        products_df,
    )

    assert set(training_df["order_id"]) == {
        "ORD-001",
        "ORD-002",
        "ORD-004",
    }

    assert "ORD-003" not in set(training_df["order_id"])


def test_training_data_creates_correct_return_label(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Returned orders should have label 1; completed orders label 0."""
    training_df = create_test_training_data(
        customers_df,
        orders_df,
        order_items_df,
        products_df,
    )

    labels_by_order = training_df.set_index(
        "order_id"
    )["return_label"].to_dict()

    assert labels_by_order["ORD-001"] == 0
    assert labels_by_order["ORD-002"] == 1
    assert labels_by_order["ORD-004"] == 0


def test_training_data_has_one_row_per_order(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Final training data must not duplicate orders after merging."""
    training_df = create_test_training_data(
        customers_df,
        orders_df,
        order_items_df,
        products_df,
    )

    assert len(training_df) == 3
    assert training_df["order_id"].nunique() == 3
    assert not training_df["order_id"].duplicated().any()


def test_training_data_contains_customer_and_product_features(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Merged training data must contain both feature groups."""
    training_df = create_test_training_data(
        customers_df,
        orders_df,
        order_items_df,
        products_df,
    )

    expected_columns = [
        "prior_order_count",
        "prior_return_rate",
        "customer_segment",
        "item_count",
        "total_quantity",
        "dominant_product_category",
    ]

    for column in expected_columns:
        assert column in training_df.columns


def test_training_data_replaces_missing_categories(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Blank text categories should become Unknown."""
    training_df = create_test_training_data(
        customers_df,
        orders_df,
        order_items_df,
        products_df,
    )

    order_four = training_df[
        training_df["order_id"] == "ORD-004"
    ].iloc[0]

    assert order_four["campaign_name"] == "Unknown"
    assert order_four["coupon_code"] == "Unknown"


def test_model_features_exclude_forbidden_columns(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
):
    """Outcome fields, IDs, and timestamps must not be model inputs."""
    training_df = create_test_training_data(
        customers_df,
        orders_df,
        order_items_df,
        products_df,
    )

    model_feature_columns = get_model_feature_columns(
        training_df
    )

    unsafe_columns = [
        column
        for column in model_feature_columns
        if column in FORBIDDEN_FEATURE_COLUMNS
    ]

    assert unsafe_columns == []
    assert "return_label" not in model_feature_columns
    assert "order_id" not in model_feature_columns
    assert "customer_id" not in model_feature_columns
    assert "order_timestamp" not in model_feature_columns