import pandas as pd
import pytest


@pytest.fixture
def customers_df() -> pd.DataFrame:
    return pd.DataFrame({
        "customer_id": ["CUST-001", "CUST-002"],
        "customer_age": [25, 40],
        "gender": ["Female", "Male"],
        "customer_segment": ["Consumer", "Corporate"],
        "customer_state": ["California", "Texas"],
        "customer_country": ["USA", "USA"],
        "region": ["West", "South"],
        "customer_acquisition_cost": [20.0, 35.0],
    })


@pytest.fixture
def orders_df() -> pd.DataFrame:
    return pd.DataFrame({
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004"],
        "customer_id": [
            "CUST-001",
            "CUST-001",
            "CUST-002",
            "CUST-002",
        ],
        "order_date": [
            "2024-01-01",
            "2024-02-01",
            "2024-03-01",
            "2024-04-01",
        ],
        "order_time": [
            "10:00:00",
            "11:00:00",
            "12:00:00",
            "13:00:00",
        ],
        "order_status": [
            "Completed",
            "Returned",
            "Pending",
            "Completed",
        ],
        "return_status": [
            None,
            "Returned",
            None,
            None,
        ],
        "net_sales": [100.0, 200.0, 150.0, 300.0],
        "discount_amount": [10.0, 20.0, 0.0, 30.0],
        "sales_channel": [
            "Website",
            "Website",
            "Mobile App",
            "Website",
        ],
        "payment_method": [
            "Credit Card",
            "Credit Card",
            "Debit Card",
            "Cash on Delivery",
        ],
        "currency": ["USD", "USD", "USD", "USD"],
        "shipping_method": [
            "Standard",
            "Express",
            "Standard",
            "Express",
        ],
        "warehouse": [
            "WH-001",
            "WH-001",
            "WH-002",
            "WH-002",
        ],
        "marketing_channel": [
            "Google Ads",
            "Google Ads",
            "Email",
            "Direct",
        ],
        "campaign_name": [
            "Campaign A",
            "Campaign A",
            None,
            None,
        ],
        "coupon_code": [
            "SAVE10",
            "SAVE10",
            None,
            None,
        ],
    })


@pytest.fixture
def products_df() -> pd.DataFrame:
    return pd.DataFrame({
        "product_id": ["PROD-001", "PROD-002"],
        "product_category": ["Electronics", "Fashion"],
        "product_subcategory": ["Phones", "Shoes"],
        "brand": ["Brand A", "Brand B"],
        "supplier": ["Supplier A", "Supplier B"],
        "product_rating": [4.5, 4.0],
    })


@pytest.fixture
def order_items_df() -> pd.DataFrame:
    return pd.DataFrame({
        "order_id": [
            "ORD-001",
            "ORD-001",
            "ORD-002",
            "ORD-003",
            "ORD-004",
        ],
        "product_id": [
            "PROD-001",
            "PROD-002",
            "PROD-001",
            "PROD-002",
            "PROD-001",
        ],
        "quantity": [1, 2, 1, 3, 2],
        "unit_price": [100.0, 50.0, 100.0, 50.0, 100.0],
        "discount_percentage": [10.0, 0.0, 10.0, 0.0, 5.0],
        "discount_amount": [10.0, 0.0, 10.0, 0.0, 10.0],
        "gross_sales": [100.0, 100.0, 100.0, 150.0, 200.0],
        "tax_amount": [5.0, 5.0, 5.0, 7.5, 10.0],
        "shipping_cost": [10.0, 10.0, 15.0, 12.0, 20.0],
        "net_sales": [105.0, 105.0, 110.0, 169.5, 220.0],
        "product_cost": [60.0, 50.0, 60.0, 75.0, 120.0],
        "profit": [45.0, 55.0, 50.0, 94.5, 100.0],
    })


@pytest.fixture
def raw_datasets(
    customers_df,
    orders_df,
    order_items_df,
    products_df,
) -> dict[str, pd.DataFrame]:
    return {
        "customers": customers_df,
        "orders": orders_df,
        "order_items": order_items_df,
        "products": products_df,
        "statistics": pd.DataFrame({
            "Total Transactions": [4],
        }),
    }