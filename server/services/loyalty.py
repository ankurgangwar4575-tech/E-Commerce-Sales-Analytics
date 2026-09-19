import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "loyalty_predictor_v1.joblib"
METADATA_PATH = MODEL_DIR / "loyalty_predictor_v1_metadata.json"

class LoyaltyPredictionService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Loyalty predictor model not found")
            
        loaded_data = joblib.load(MODEL_PATH)
        self.model = loaded_data['model']
        self.features = loaded_data['features']
        self.cat_features = loaded_data['cat_features']
        
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)

    def predict(self, request_data: dict) -> dict:
        try:
            df = pd.DataFrame([request_data])
            
            for col in self.cat_features:
                if col in self.metadata['label_encoders']:
                    encoder_dict = self.metadata['label_encoders'][col]
                    val = str(df[col].iloc[0])
                    if val in encoder_dict:
                        df[col] = encoder_dict[val]
                    else:
                        df[col] = 0 
                
            X = df[self.features]
            
            predicted_points = self.model.predict(X)[0]
            predicted_points = max(0.0, float(predicted_points))
            
            return {
                "predicted_points": predicted_points
            }
            
        except Exception as e:
            print(f"Error in loyalty prediction: {str(e)}")
            raise e
