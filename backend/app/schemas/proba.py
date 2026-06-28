from pydantic import BaseModel, Field
from typing import Dict, List

class ProbaBase(BaseModel):
    ouvrage_id: int
    pathologie_code: str
    probability: float = Field(..., ge=0.0, le=1.0)
    classification: str = Field(..., description="Low, Moderate, High, Very High")

class ProbaResponse(ProbaBase):
    id: int

    class Config:
        from_attributes = True

class ProbaMatrix(BaseModel):
    ouvrage_id: int
    probabilities: Dict[str, float]  # mapping pathologie_code -> probability (e.g. 'P1' -> 0.45)
