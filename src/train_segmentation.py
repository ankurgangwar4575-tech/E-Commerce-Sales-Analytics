import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import json

from src.config import ensure_project_directories

MODELS_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

def train_segmentation_model():
    ensure_project_directories()
    
    print("Loading data for segmentation...")
    customers_df = pd.read_csv(DATA_DIR / "customer_master.csv")
    orders_df = pd.read_csv(DATA_DIR / "ecommerce_sales_customer_analytics_150k.csv")
    
    print("Computing customer lifetime value metrics...")
    # Group orders by customer
    ltv_df = orders_df.groupby("customer_id").agg(
        total_orders=("order_id", "count"),
        total_spend=("net_sales", "sum"),
        total_returns=("return_status", lambda x: (x == "Returned").sum())
    ).reset_index()
    
    ltv_df["return_rate"] = ltv_df["total_returns"] / ltv_df["total_orders"]
    
    # Merge with customer static data
    segmentation_df = ltv_df.merge(customers_df[["customer_id", "customer_age", "customer_acquisition_cost"]], on="customer_id", how="left")
    
    # Fill any NaNs
    segmentation_df.fillna(0, inplace=True)
    
    # Select features for clustering
    features = ["total_orders", "total_spend", "return_rate", "customer_age", "customer_acquisition_cost"]
    X = segmentation_df[features]
    
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("Training KMeans clustering (k=3)...")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    segmentation_df["cluster"] = kmeans.labels_
    
    print("Saving models...")
    joblib.dump(scaler, MODELS_DIR / "segmentation_scaler.joblib")
    joblib.dump(kmeans, MODELS_DIR / "customer_segmentation_v1.joblib")
    
    metadata = {
        "model_version": "customer_segmentation_v1",
        "model_name": "KMeans",
        "n_clusters": 3,
        "features": features,
        "cluster_profiles": {
            0: "Occasional Shoppers",
            1: "High-Value Loyalists",
            2: "High-Return/At-Risk Shoppers"
        }
    }
    
    with open(MODELS_DIR / "customer_segmentation_v1_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Customer segmentation training complete!")

if __name__ == "__main__":
    train_segmentation_model()
