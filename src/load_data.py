from pathlib import Path

import pandas as pd

from src.config import DATA_DIR


RAW_DATA_FILES = {
    "customers": DATA_DIR / "customer_master.csv",
    "orders": DATA_DIR / "ecommerce_sales_customer_analytics_150k.csv",
    "order_items": DATA_DIR / "order_items.csv",
    "products": DATA_DIR / "product_catalog.csv",
    "statistics": DATA_DIR / "dataset_statistics.csv",
}


def load_raw_datasets() -> dict[str, pd.DataFrame]:
    """
    Load all approved raw CSV datasets.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing customers, orders, order_items,
        products, and statistics DataFrames.
    """
    missing_files = [
        name
        for name, path in RAW_DATA_FILES.items()
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required data files: "
            + ", ".join(missing_files)
        )

    datasets = {
        name: pd.read_csv(path)
        for name, path in RAW_DATA_FILES.items()
    }

    return datasets


def create_dataset_summary(
    datasets: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Create a small summary table for loaded datasets.
    """
    summary_rows = []

    for name, dataframe in datasets.items():
        summary_rows.append({
            "dataset": name,
            "rows": len(dataframe),
            "columns": dataframe.shape[1],
            "memory_mb": round(
                dataframe.memory_usage(deep=True).sum()
                / (1024 ** 2),
                2,
            ),
        })

    return pd.DataFrame(summary_rows)


if __name__ == "__main__":
    raw_datasets = load_raw_datasets()
    summary_df = create_dataset_summary(raw_datasets)

    print(summary_df.to_string(index=False))