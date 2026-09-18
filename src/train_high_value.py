import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import json

from src.config import ensure_project_directories

MODELS_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

def train_high_value_model():
    ensure_project_directories()
    
    print("Loading data for High-Value Detection...")
    customers_df = pd.read_csv(DATA_DIR / "customer_master.csv")
    orders_df = pd.read_csv(DATA_DIR / "ecommerce_sales_customer_analytics_150k.csv")
    
    ltv_df = orders_df.groupby("customer_id").agg(
        total_spend=("net_sales", "sum"),
        total_orders=("order_id", "count")
    ).reset_index()
    
    threshold = ltv_df['total_spend'].quantile(0.80)
    print(f"High-Value Threshold (Top 20%): ${threshold:.2f}")
    ltv_df['is_high_value'] = (ltv_df['total_spend'] >= threshold).astype(int)
    
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
    first_orders = orders_df.sort_values('order_date').groupby('customer_id').first().reset_index()
    
    first_orders = first_orders.rename(columns={
        'net_sales': 'first_order_value',
        'discount_amount': 'first_order_discount',
        'quantity': 'first_order_quantity',
        'sales_channel': 'first_order_channel'
    })
    
    df = customers_df.merge(ltv_df[['customer_id', 'is_high_value']], on='customer_id')
    df = df.merge(first_orders[['customer_id', 'first_order_value', 'first_order_discount', 'first_order_quantity', 'first_order_channel']], on='customer_id')
    
    features = [
        'customer_age', 
        'customer_acquisition_cost', 
        'first_order_value', 
        'first_order_discount', 
        'first_order_quantity'
    ]
    
    df['gender'] = df['gender'].astype('category').cat.codes
    df['first_order_channel'] = df['first_order_channel'].astype('category').cat.codes
    
    categorical_features = ['gender', 'first_order_channel']
    all_features = features + categorical_features
    
    X = df[all_features]
    y = df['is_high_value']
    
    print("Training LightGBM model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        random_state=42,
        verbosity=-1
    )
    
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)])
    
    print("Saving model and metadata...")
    model_data = {
        'model': model
    }
    joblib.dump(model_data, MODELS_DIR / "high_value_v1.joblib")
    
    metadata = {
        "model_version": "high_value_v1",
        "model_name": "LightGBM Classifier",
        "features": all_features,
        "categorical_columns": categorical_features,
        "ltv_threshold": threshold
    }
    
    with open(MODELS_DIR / "high_value_v1_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("High-Value model training complete!")

if __name__ == "__main__":
    train_high_value_model()
