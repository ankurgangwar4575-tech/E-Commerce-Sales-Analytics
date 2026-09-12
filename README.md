# E-Commerce Return Risk Model

This project builds a machine-learning model that predicts whether an e-commerce order is likely to be returned. The work is shared by two contributors and uses order, customer, order-item, and product data.

## Project goal

The first model will score each order at order placement as either likely to be returned or unlikely to be returned. The target is derived from `return_status` in the main order dataset.

## Data

The approved source data is committed in `data/` so both contributors work from the same inputs.

| File | Description | Key |
| --- | --- | --- |
| `customer_master.csv` | Customer demographics, segments, locations, and acquisition cost | `customer_id` |
| `ecommerce_sales_customer_analytics_150k.csv` | Main order-level data and return label | `order_id`, `customer_id` |
| `order_items.csv` | Products, quantities, prices, discounts, and margins per order item | `order_id`, `product_id` |
| `product_catalog.csv` | Product, category, brand, supplier, and rating details | `product_id` |
| `dataset_statistics.csv` | Dataset-level summary statistics | Reference only |

## Planned layout

```text
data/       Shared source CSV files
src/        Reusable feature engineering, training, and evaluation code
tests/      Automated checks for feature engineering and data joins
notebooks/  Exploratory analysis only
models/     Final versioned trained models and model metadata
images/     README charts and diagrams
```

## Team workflow

1. Create a branch for each task.
2. Keep reusable logic in `src/`, not only in notebooks.
3. Push code, approved source data, final model files, and model metadata to GitHub.
4. Open a pull request before merging work into `main`.
5. Do not commit secrets, local environments, temporary outputs, or experiment logs.

Suggested task split:

- Customer contributor: customer features from `customer_master.csv` and prior-order history.
- Product contributor: item and product features from `order_items.csv` and `product_catalog.csv`.
- Joint work: merge features at `order_id`, train, evaluate, and version the final model.

## Modelling rules

Use one row per `order_id` in the final training dataset. Split training, validation, and test data chronologically, rather than randomly.

Do not use information that becomes available after an order outcome. Exclude `return_status`, `return_reason`, actual delivery fields, customer reviews, review sentiment, and post-order payment outcomes from the feature set.

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## First milestone

Build the merged, leakage-safe training dataset with customer, order, item, and product features. Train a logistic-regression baseline before comparing it with a gradient-boosting model such as CatBoost.
