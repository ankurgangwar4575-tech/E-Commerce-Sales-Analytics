import json
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent / "models"
FORECAST_PATH = MODEL_DIR / "sales_forecast_v1.json"

class ForecastService:
    def __init__(self):
        if not FORECAST_PATH.exists():
            raise FileNotFoundError("Sales forecast data not found")
            
        with open(FORECAST_PATH, "r") as f:
            self.forecast_data = json.load(f)
            
    def get_forecast(self) -> dict:
        return self.forecast_data