from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from server.schemas import PredictionRequest, PredictionResponse, SegmentationRequest, SegmentationResponse, HighValueRequest, HighValueResponse, RatingRequest, RatingResponse
from server.services.prediction import PredictionService
from server.services.segmentation import SegmentationService
from server.services.high_value import HighValueService
from server.services.rating import RatingService
from server.services.forecast import ForecastService

app = FastAPI(
    title="Return Risk Prediction API",
    description="API for scoring e-commerce orders for return risk using a LightGBM model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    prediction_service = PredictionService()
except Exception as e:
    print(f"Warning: Failed to load prediction service on startup. Error: {e}")
    prediction_service = None

try:
    segmentation_service = SegmentationService()
except Exception as e:
    print(f"Warning: Failed to load segmentation service on startup. Error: {e}")
    segmentation_service = None

try:
    high_value_service = HighValueService()
except Exception as e:
    print(f"Warning: Failed to load high value service on startup. Error: {e}")
    high_value_service = None

try:
    rating_service = RatingService()
except Exception as e:
    print(f"Warning: Failed to load rating service on startup. Error: {e}")
    rating_service = None

try:
    forecast_service = ForecastService()
except Exception as e:
    print(f"Warning: Failed to load forecast service on startup. Error: {e}")
    forecast_service = None

@app.get("/")
def root():
    return {"message": "Welcome to the Return Risk Prediction API"}

@app.get("/stats")
def get_stats():
    stats_path = Path(__file__).parent.parent / "data" / "dataset_statistics.csv"
    if not stats_path.exists():
        raise HTTPException(status_code=404, detail="Stats file not found")
    
    try:
        df = pd.read_csv(stats_path)
        stats_dict = df.iloc[0].to_dict()
        return stats_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read stats: {str(e)}")

@app.get("/health")
def health_check():
    status = "healthy" if prediction_service is not None else "degraded"
    return {"status": status, "model_loaded": prediction_service is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict_risk(request: PredictionRequest):
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service is not available")
    
    try:
        response = prediction_service.predict(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@app.post("/segment", response_model=SegmentationResponse)
def segment_customer(request: SegmentationRequest):
    if segmentation_service is None:
        raise HTTPException(status_code=503, detail="Segmentation service is not available")
    
    try:
        response = segmentation_service.segment(request.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Segmentation failed: {str(e)}")

@app.post("/high-value", response_model=HighValueResponse)
def predict_high_value(request: HighValueRequest):
    if high_value_service is None:
        raise HTTPException(status_code=503, detail="High-Value service is not available")
    
    try:
        response = high_value_service.predict(request.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"High-Value Prediction failed: {str(e)}")

@app.post("/rating", response_model=RatingResponse)
def predict_rating(request: RatingRequest):
    if rating_service is None:
        raise HTTPException(status_code=503, detail="Rating service is not available")
    
    try:
        response = rating_service.predict(request.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Rating Prediction failed: {str(e)}")

@app.get("/forecast")
def get_forecast():
    if forecast_service is None:
        raise HTTPException(status_code=503, detail="Forecast service is not available")
    
    try:
        return forecast_service.get_forecast()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch forecast: {str(e)}")
