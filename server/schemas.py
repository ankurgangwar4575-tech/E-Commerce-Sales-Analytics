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

class SegmentClassifyRequest(BaseModel):
    gender: str
    region: str
    customer_age: int
    discount_amount: float
    gross_sales: float
    shipping_cost: float

class SegmentProb(BaseModel):
    segment: str
    probability: float

class SegmentClassifyResponse(BaseModel):
    predicted_segment: str
    probabilities: list[SegmentProb]

class LoyaltyRequest(BaseModel):
    customer_segment: str
    payment_method: str
    gross_sales: float
    discount_amount: float
    quantity: int

class LoyaltyResponse(BaseModel):
    predicted_points: float

class ReturnReasonRequest(BaseModel):
    customer_segment: str
    shipping_method: str
    customer_age: int
    gross_sales: float
    discount_amount: float

class ReasonProb(BaseModel):
    reason: str
    probability: float

class ReturnReasonResponse(BaseModel):
    predicted_reason: str
    probabilities: list[ReasonProb]

class SentimentRequest(BaseModel):
    order_status: str
    return_status: str
    delivery_days: float
    estimated_delivery_days: float
    discount_amount: float
    gross_sales: float

class SentimentProb(BaseModel):
    sentiment: str
    probability: float

class SentimentResponse(BaseModel):
    predicted_sentiment: str
    probabilities: list[SentimentProb]
