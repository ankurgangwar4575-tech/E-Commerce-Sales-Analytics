import pandas as pd
import pytest

from src import load_data


def test_load_raw_datasets(
    raw_datasets,
    tmp_path,
    monkeypatch,
):
    """All CSV files should load into the expected dictionary."""
    test_file_paths = {}

    for dataset_name, dataframe in raw_datasets.items():
        file_path = tmp_path / f"{dataset_name}.csv"

        dataframe.to_csv(file_path, index=False)

        test_file_paths[dataset_name] = file_path

    monkeypatch.setattr(
        load_data,
        "RAW_DATA_FILES",
        test_file_paths,
    )

    loaded_datasets = load_data.load_raw_datasets()

    assert set(loaded_datasets.keys()) == {
        "customers",
        "orders",
        "order_items",
        "products",
        "statistics",
    }

    assert len(loaded_datasets["customers"]) == 2
    assert len(loaded_datasets["orders"]) == 4
    assert len(loaded_datasets["order_items"]) == 5
    assert len(loaded_datasets["products"]) == 2


def test_load_raw_datasets_raises_error_when_file_missing(
    tmp_path,
    monkeypatch,
):
    """Loading should stop if even one required file is missing."""
    missing_file_paths = {
        "customers": tmp_path / "customers.csv",
        "orders": tmp_path / "orders.csv",
        "order_items": tmp_path / "order_items.csv",
        "products": tmp_path / "products.csv",
        "statistics": tmp_path / "statistics.csv",
    }

    monkeypatch.setattr(
        load_data,
        "RAW_DATA_FILES",
        missing_file_paths,
    )

    with pytest.raises(
        FileNotFoundError,
        match="Missing required data files",
    ):
        load_data.load_raw_datasets()


def test_create_dataset_summary(raw_datasets):
    """Dataset summary should report one row for each dataset."""
    summary_df = load_data.create_dataset_summary(
        raw_datasets
    )

    assert len(summary_df) == 5

    assert set(summary_df.columns) == {
        "dataset",
        "rows",
        "columns",
        "memory_mb",
    }

    orders_summary = summary_df[
        summary_df["dataset"] == "orders"
    ].iloc[0]

    assert orders_summary["rows"] == 4
    assert orders_summary["columns"] == 16