import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "delay_classifier_v1.joblib"
METADATA_PATH = MODEL_DIR / "delay_classifier_v1_metadata.json"

class DelayService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Delay Classifier model not found")
            
        loaded_data = joblib.load(MODEL_PATH)
        self.model = loaded_data['model']
        
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)
            
        self.features = self.metadata["features"]
        self.cat_features = self.metadata["cat_features"]
        self.label_encoders = self.metadata["label_encoders"]
        
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
        delay_prob = float(probas[1])
        
        is_high_risk = delay_prob > 0.5
        
        return {
            "delay_probability": round(delay_prob, 4),
            "is_high_risk": is_high_risk
        }
