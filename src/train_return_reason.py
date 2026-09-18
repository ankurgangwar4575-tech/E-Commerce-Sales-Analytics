import pandas as pd
import json
import joblib
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def train_return_reason():
    print("Loading data for Return Reason Predictor...")
    data_path = Path("data/ecommerce_sales_customer_analytics_150k.csv")
    df = pd.read_csv(data_path)
    
    # Filter only for items that were returned (assuming return_status == 'Returned')
    # Or just drop NaN in return_reason
    df = df.dropna(subset=['return_reason'])
    
    cat_features = ['customer_segment', 'shipping_method']
    num_features = ['customer_age', 'gross_sales', 'discount_amount']
    features = cat_features + num_features
    target = 'return_reason'
    
    df = df.dropna(subset=features + [target])
    
    # Encode categorical features
    label_encoders = {}
    for col in cat_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = {str(cls): int(idx) for idx, cls in enumerate(le.classes_)}
        
    # Encode target
    target_le = LabelEncoder()
    y = target_le.fit_transform(df[target])
    target_classes = list(target_le.classes_)
    
    X = df[features]
    
    print("Training LightGBM Multi-class Classifier...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
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
    
    print(f"Model Evaluation - Accuracy: {acc:.4f}")
    
    print("Saving model and metadata...")
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "return_reason_classifier_v1.joblib"
    joblib.dump({"model": model}, model_path)
    
    metadata = {
        "features": features,
        "cat_features": cat_features,
        "label_encoders": label_encoders,
        "target_classes": target_classes,
        "model_type": "LightGBM Classifier",
        "metrics": {
            "accuracy": float(acc)
        }
    }
    
    with open(model_dir / "return_reason_classifier_v1_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Return Reason Predictor model training complete!")

if __name__ == "__main__":
    train_return_reason()
