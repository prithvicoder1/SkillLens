from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
predicted_category: str = Field(
…,
description=“Predicted insurance premium category”
)

confidence: float = Field(
    ...,
    ge=0.0,
    le=1.0,
    description="Confidence score of the prediction"
)
class_probabilities: Dict[str, float] = Field(
    ...,
    description="Probability distribution across all classes"
)