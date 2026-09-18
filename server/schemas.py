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

class SegmentationRequest(BaseModel):
    total_orders: int
    total_spend: float
    return_rate: float
    customer_age: int
    customer_acquisition_cost: float

class SegmentationResponse(BaseModel):
    cluster_id: int
    profile: str

class HighValueRequest(BaseModel):
    customer_age: int
    customer_acquisition_cost: float
    first_order_value: float
    first_order_discount: float
    first_order_quantity: int
    gender: str
    first_order_channel: str

class HighValueResponse(BaseModel):
    high_value_probability: float
    is_high_value: bool

class RatingRequest(BaseModel):
    delivery_days: int
    estimated_delivery_days: int
    discount_amount: float
    shipping_cost: float
    gross_sales: float

class RatingResponse(BaseModel):
    predicted_rating: float
