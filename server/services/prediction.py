import json
from pathlib import Path
import joblib
import pandas as pd
from server.schemas import PredictionRequest, PredictionResponse

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_PATH = MODEL_DIR / "return_risk_v1.joblib"
METADATA_PATH = MODEL_DIR / "return_risk_v1_metadata.json"

class PredictionService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        self.model = joblib.load(MODEL_PATH)

        if not METADATA_PATH.exists():
            raise FileNotFoundError(f"Metadata file not found at {METADATA_PATH}")
        with open(METADATA_PATH, "r") as f:
            self.metadata = json.load(f)

        self.feature_columns = self.metadata["feature_columns"]
        self.categorical_columns = self.metadata.get("categorical_columns", [])
        self.threshold = self.metadata.get("decision_threshold", 0.7)

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        input_data = {col: request.features.get(col) for col in self.feature_columns}
        df = pd.DataFrame([input_data])
        
        for col in self.categorical_columns:
            if col in df.columns:
                df[col] = df[col].astype('category')

        probabilities = self.model.predict_proba(df)
        risk_score = float(probabilities[0][1])  # Class 1 is 'returned'

        is_high_risk = risk_score >= self.threshold

        return PredictionResponse(
            risk_score=risk_score,
            is_high_risk=is_high_risk
        )
