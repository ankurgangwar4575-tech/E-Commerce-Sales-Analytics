import pandas as pd
import pytest

from src.validate_data import (
    raise_if_data_quality_fails,
    validate_data_quality,
    validate_required_columns,
)


def test_valid_datasets_pass_all_quality_checks(
    raw_datasets,
):
    """The valid fixture data should pass every quality check."""
    quality_report_df = validate_data_quality(raw_datasets)

    assert not quality_report_df.empty
    assert set(quality_report_df["status"]) == {"PASS"}


def test_required_columns_check_finds_missing_column(
    raw_datasets,
):
    """Missing required columns should produce a FAIL result."""
    invalid_datasets = raw_datasets.copy()

    invalid_datasets["orders"] = raw_datasets["orders"].drop(
        columns=["return_status"]
    )

    required_columns_report = validate_required_columns(
        invalid_datasets
    )

    orders_result = next(
        result
        for result in required_columns_report
        if result["check"] == "orders: required columns"
    )

    assert orders_result["status"] == "FAIL"
    assert "return_status" in orders_result["details"]


def test_invalid_customer_relationship_fails(
    raw_datasets,
):
    """An order with an unknown customer must fail validation."""
    invalid_datasets = raw_datasets.copy()

    invalid_orders_df = raw_datasets["orders"].copy()
    invalid_orders_df.loc[
        invalid_orders_df["order_id"] == "ORD-001",
        "customer_id",
    ] = "CUST-UNKNOWN"

    invalid_datasets["orders"] = invalid_orders_df

    quality_report_df = validate_data_quality(
        invalid_datasets
    )

    customer_join_result = quality_report_df[
        quality_report_df["check"]
        == "Orders have valid customers"
    ].iloc[0]

    assert customer_join_result["status"] == "FAIL"
    assert customer_join_result["value"] == 1


def test_duplicate_order_id_fails(
    raw_datasets,
):
    """Duplicate order IDs must fail validation."""
    invalid_datasets = raw_datasets.copy()

    invalid_orders_df = pd.concat(
        [
            raw_datasets["orders"],
            raw_datasets["orders"].iloc[[0]],
        ],
        ignore_index=True,
    )

    invalid_datasets["orders"] = invalid_orders_df

    quality_report_df = validate_data_quality(
        invalid_datasets
    )

    duplicate_order_result = quality_report_df[
        quality_report_df["check"] == "Order IDs are unique"
    ].iloc[0]

    assert duplicate_order_result["status"] == "FAIL"
    assert duplicate_order_result["value"] == 1


def test_raise_if_data_quality_fails_raises_error(
    raw_datasets,
):
    """The pipeline should stop if a critical check fails."""
    invalid_datasets = raw_datasets.copy()

    invalid_orders_df = raw_datasets["orders"].copy()
    invalid_orders_df.loc[
        invalid_orders_df["order_id"] == "ORD-001",
        "customer_id",
    ] = "CUST-UNKNOWN"

    invalid_datasets["orders"] = invalid_orders_df

    quality_report_df = validate_data_quality(
        invalid_datasets
    )

    with pytest.raises(
        ValueError,
        match="Data quality validation failed",
    ):
        raise_if_data_quality_fails(quality_report_df)