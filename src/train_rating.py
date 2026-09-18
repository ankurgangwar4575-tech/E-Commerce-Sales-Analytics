import pandas as pd
import json
import joblib
from pathlib import Path
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

def train_rating_model():
    print("Loading data for Rating Prediction...")
    data_path = Path("data/ecommerce_sales_customer_analytics_150k.csv")
    df = pd.read_csv(data_path)
    
    df['is_late'] = (df['delivery_days'] > df['estimated_delivery_days']).astype(int)
    
    features = [
        'delivery_days',
        'estimated_delivery_days',
        'is_late',
        'discount_amount',
        'shipping_cost',
        'gross_sales'
    ]
    
    target = 'customer_rating'
    
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    
    print("Training LightGBM Regressor for Rating Prediction...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LGBMRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)])
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model Evaluation - MSE: {mse:.4f}, MAE: {mae:.4f}")
    
    print("Saving model and metadata...")
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "rating_prediction_v1.joblib"
    joblib.dump({"model": model}, model_path)
    
    metadata = {
        "features": features,
        "model_type": "LightGBM Regressor",
        "description": "Predicts customer rating (1-5) based on order characteristics.",
        "metrics": {
            "mse": float(mse),
            "mae": float(mae)
        }
    }
    
    with open(model_dir / "rating_prediction_v1_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Rating Prediction model training complete!")

if __name__ == "__main__":
    train_rating_model()