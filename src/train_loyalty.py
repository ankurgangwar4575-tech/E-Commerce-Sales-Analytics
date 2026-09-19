import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from lightgbm import LGBMRegressor
import joblib
import json

def train_loyalty_predictor():
    print("Loading dataset...")
    data_path = Path("data/ecommerce_sales_customer_analytics_150k.csv")
    df = pd.read_csv(data_path)
    
    target = 'loyalty_points_earned'
    df = df.dropna(subset=[target])
    
    cat_features = ['customer_segment', 'payment_method']
    num_features = ['gross_sales', 'discount_amount', 'quantity']
    features = cat_features + num_features
    
    df = df.dropna(subset=features + [target])
    
    label_encoders = {}
    for col in cat_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = {str(cls): int(idx) for idx, cls in enumerate(le.classes_)}
        
    X = df[features]
    y = df[target]
    
    print("Training LightGBM Regressor for Loyalty Points...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LGBMRegressor(
        n_estimators=100,
        learning_rate=0.05,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.4f}")
    
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "loyalty_predictor_v1.joblib"
    joblib.dump({
        'model': model,
        'features': features,
        'cat_features': cat_features
    }, model_path)
    
    metadata = {
        'features': features,
        'cat_features': cat_features,
        'label_encoders': label_encoders
    }
    
    metadata_path = model_dir / "loyalty_predictor_v1_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Model saved to {model_path}")
    print(f"Metadata saved to {metadata_path}")

if __name__ == "__main__":
    train_loyalty_predictor()
