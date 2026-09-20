from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from server.schemas import PredictionRequest, PredictionResponse, SegmentationRequest, SegmentationResponse, HighValueRequest, HighValueResponse, RatingRequest, RatingResponse, SegmentClassifyRequest, SegmentClassifyResponse, ReturnReasonRequest, ReturnReasonResponse, SentimentRequest, SentimentResponse, LoyaltyRequest, LoyaltyResponse
from server.services.prediction import PredictionService
from server.services.segmentation import SegmentationService 
from server.services.high_value import HighValueService
from server.services.rating import RatingService
from server.services.forecast import ForecastService
from server.services.segment_classifier import SegmentClassifierService
from server.services.return_reason import ReturnReasonService
from server.services.sentiment import SentimentService
from server.services.loyalty import LoyaltyPredictionService

app = FastAPI(
    title="Return Risk Prediction API",
    description="API for scoring e-commerce orders for return risk using a LightGBM model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://saless-analyticss.vercel.app"],
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

try:
    segment_classifier_service = SegmentClassifierService()
except Exception as e:
    print(f"Warning: Failed to load segment classifier service on startup. Error: {e}")
    segment_classifier_service = None

try:
    return_reason_service = ReturnReasonService()
except Exception as e:
    print(f"Warning: Failed to load return reason service on startup. Error: {e}")
    return_reason_service = None

try:
    sentiment_service = SentimentService()
except Exception as e:
    print(f"Warning: Failed to load sentiment service on startup. Error: {e}")
    sentiment_service = None

try:
    loyalty_service = LoyaltyPredictionService()
except Exception as e:
    print(f"Warning: Failed to load loyalty service on startup. Error: {e}")
    loyalty_service = None

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

@app.post("/predict-segment", response_model=SegmentClassifyResponse)
def predict_segment(request: SegmentClassifyRequest):
    if segment_classifier_service is None:
        raise HTTPException(status_code=503, detail="Segment classifier service is not available")
    
    try:
        response = segment_classifier_service.predict(request.model_dump())
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Segment classification failed: {str(e)}")

@app.post("/predict-return-reason", response_model=ReturnReasonResponse)
def predict_return_reason(request: ReturnReasonRequest):
    if return_reason_service is None:
        raise HTTPException(status_code=503, detail="Return reason service is not available")
    
    try:
        return return_reason_service.predict(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Return reason prediction failed: {str(e)}")

@app.post("/predict-sentiment", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest):
    if sentiment_service is None:
        raise HTTPException(status_code=503, detail="Sentiment service is not available")
    
    try:
        return sentiment_service.predict(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sentiment prediction failed: {str(e)}")

@app.post("/predict-loyalty", response_model=LoyaltyResponse)
def predict_loyalty(request: LoyaltyRequest):
    if loyalty_service is None:
        raise HTTPException(status_code=503, detail="Loyalty service is not available")
    
    try:
        return loyalty_service.predict(request.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Loyalty prediction failed: {str(e)}")
