import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "rating_prediction_v1.joblib"
METADATA_PATH = MODEL_DIR / "rating_prediction_v1_metadata.json"

class RatingService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Rating Prediction model not found")
            
        loaded_data = joblib.load(MODEL_PATH)
        self.model = loaded_data['model']
        
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)
            
        self.features = self.metadata["features"]
        
    def predict(self, data: dict) -> dict:
        if 'is_late' not in data:
            data['is_late'] = 1 if float(data.get('delivery_days', 0)) > float(data.get('estimated_delivery_days', 0)) else 0
            
        df = pd.DataFrame([data])
        X = df[self.features]
        
        rating = float(self.model.predict(X)[0])
        rating = max(1.0, min(5.0, rating))
        
        return {
            "predicted_rating": round(rating, 1)
        }