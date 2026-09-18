import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "high_value_v1.joblib"
METADATA_PATH = MODEL_DIR / "high_value_v1_metadata.json"

class HighValueService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError("High-Value model not found")
            
        loaded_data = joblib.load(MODEL_PATH)
        self.model = loaded_data['model']
        
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)
            
        self.features = self.metadata["features"]
        self.categorical_columns = self.metadata["categorical_columns"]
        
    def predict(self, data: dict) -> dict:
        # Map categorical strings to codes for prediction
        # For simplicity in this demo, gender mapping: F=0, M=1, Other=2
        # Channel mapping: App=0, In-Store=1, Online=2
        
        # We will do a robust manual mapping based on typical sorting
        gender_map = {'F': 0, 'M': 1, 'Other': 2}
        channel_map = {'App': 0, 'In-Store': 1, 'Online': 2}
        
        if 'gender' in data and isinstance(data['gender'], str):
            data['gender'] = gender_map.get(data['gender'], 0)
            
        if 'first_order_channel' in data and isinstance(data['first_order_channel'], str):
            data['first_order_channel'] = channel_map.get(data['first_order_channel'], 2)

        df = pd.DataFrame([data])
        X = df[self.features]
        
        # Predict probability of class 1 (High-Value)
        prob = float(self.model.predict_proba(X)[0][1])
        
        return {
            "high_value_probability": prob,
            "is_high_value": prob > 0.5
        }
