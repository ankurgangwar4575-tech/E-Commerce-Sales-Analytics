import json
import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
KMEANS_PATH = MODEL_DIR / "customer_segmentation_v1.joblib"
SCALER_PATH = MODEL_DIR / "segmentation_scaler.joblib"
METADATA_PATH = MODEL_DIR / "customer_segmentation_v1_metadata.json"

class SegmentationService:
    def __init__(self):
        if not KMEANS_PATH.exists() or not SCALER_PATH.exists():
            raise FileNotFoundError("Segmentation models not found")
            
        self.model = joblib.load(KMEANS_PATH)
        self.scaler = joblib.load(SCALER_PATH)
        
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)
            
        self.features = self.metadata["features"]
        self.profiles = self.metadata["cluster_profiles"]
        
    def segment(self, data: dict) -> dict:
        df = pd.DataFrame([data])
        X = df[self.features]

        X_scaled = self.scaler.transform(X)
    
        cluster_id = int(self.model.predict(X_scaled)[0])
        profile = self.profiles[str(cluster_id)]
        
        return {
            "cluster_id": cluster_id,
            "profile": profile
        }
