from typing import Any, Dict
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    features: Dict[str, Any] = Field(
        ..., 
        description="Dictionary containing the 50 feature columns required by the model."
    )

class PredictionResponse(BaseModel):
    risk_score: float = Field(..., description="Probability of the order being returned (0.0 to 1.0)")
    is_high_risk: bool = Field(..., description="True if risk_score >= threshold, else False")
