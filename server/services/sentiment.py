import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "sentiment_classifier_v1.joblib"
METADATA_PATH = MODEL_DIR / "sentiment_classifier_v1_metadata.json"

class SentimentService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Sentiment Classifier model not found")
            
        loaded_data = joblib.load(MODEL_PATH)
        self.model = loaded_data['model']
        
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)
            
        self.features = self.metadata["features"]
        self.cat_features = self.metadata["cat_features"]
        self.label_encoders = self.metadata["label_encoders"]
        self.target_classes = self.metadata["target_classes"]
        
    def predict(self, data: dict) -> dict:
        df = pd.DataFrame([data])
        
        for col in self.cat_features:
            val = str(df[col].iloc[0])
            mapping = self.label_encoders[col]
            if val in mapping:
                df[col] = mapping[val]
            else:
                df[col] = 0
                
        X = df[self.features]
        
        probas = self.model.predict_proba(X)[0]
        
        results = []
        for i, class_name in enumerate(self.target_classes):
            results.append({
                "sentiment": class_name,
                "probability": round(float(probas[i]), 4)
            })
            
        results.sort(key=lambda x: x["probability"], reverse=True)
        
        return {
            "predicted_sentiment": results[0]["sentiment"],
            "probabilities": results
        }
