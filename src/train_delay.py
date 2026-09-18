import pandas as pd
import json
import joblib
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

def train_delay_model():
    print("Loading data for Delivery Delay Classification...")
    data_path = Path("data/ecommerce_sales_customer_analytics_150k.csv")
    df = pd.read_csv(data_path)
    
    # Create target: 1 if delivery_days > estimated_delivery_days, else 0
    df = df.dropna(subset=['delivery_days', 'estimated_delivery_days'])
    df['is_delayed'] = (df['delivery_days'] > df['estimated_delivery_days']).astype(int)
    
    cat_features = ['shipping_method', 'warehouse', 'region', 'customer_country']
    num_features = ['shipping_cost']
    features = cat_features + num_features
    target = 'is_delayed'
    
    df = df.dropna(subset=features + [target])
    
    # Encode categorical features
    label_encoders = {}
    for col in cat_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = {str(cls): int(idx) for idx, cls in enumerate(le.classes_)}
        
    X = df[features]
    y = df[target]
    
    print("Training LightGBM Binary Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(
        X_train, y_train, 
        eval_set=[(X_test, y_test)],
        categorical_feature=cat_features
    )
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    
    print(f"Model Evaluation - Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}")
    
    print("Saving model and metadata...")
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "delay_classifier_v1.joblib"
    joblib.dump({"model": model}, model_path)
    
    metadata = {
        "features": features,
        "cat_features": cat_features,
        "label_encoders": label_encoders,
        "model_type": "LightGBM Binary Classifier",
        "metrics": {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec)
        }
    }
    
    with open(model_dir / "delay_classifier_v1_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Delivery Delay model training complete!")

if __name__ == "__main__":
    train_delay_model()
