from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from server.schemas import PredictionRequest, PredictionResponse
from server.services.prediction import PredictionService

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

@app.get("/")
def root():
    return {"message": "Welcome to the Return Risk Prediction API"}

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
