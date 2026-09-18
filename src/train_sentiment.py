import pandas as pd
import json
import joblib
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def train_sentiment_model():
    print("Loading data for Review Sentiment Analyzer...")
    data_path = Path("data/ecommerce_sales_customer_analytics_150k.csv")
    df = pd.read_csv(data_path)
    
    df = df.dropna(subset=['review_sentiment'])
    
    df['return_status'] = df['return_status'].fillna('Not Returned')
    
    cat_features = ['order_status', 'return_status']
    num_features = ['delivery_days', 'estimated_delivery_days', 'discount_amount', 'gross_sales']
    features = cat_features + num_features
    target = 'review_sentiment'
    
    df = df.dropna(subset=features + [target])
    
    label_encoders = {}
    for col in cat_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = {str(cls): int(idx) for idx, cls in enumerate(le.classes_)}
        
    target_le = LabelEncoder()
    y = target_le.fit_transform(df[target])
    target_classes = list(target_le.classes_)
    
    X = df[features]
    
    print("Training LightGBM Multi-class Classifier (Balanced)...")
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
    
    print(f"Model Evaluation - Accuracy: {acc:.4f}")
    
    print("Saving model and metadata...")
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "sentiment_classifier_v1.joblib"
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
    
    with open(model_dir / "sentiment_classifier_v1_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Sentiment Classifier model training complete!")

if __name__ == "__main__":
    train_sentiment_model()
