from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InsarPointBase(BaseModel):
    lat: float
    lon: float
    vitesse_los: float
    cumul: float
    
class InsarPointResponse(InsarPointBase):
    id: int
    ouvrage_id: Optional[int]
    acceleration: Optional[float]
    anomaly_score: Optional[float]
    consensus_level: Optional[int]
    cluster_id: Optional[int]
    is_anomaly_iso: Optional[bool]
    
    class Config:
        from_attributes = True

class InsarCluster(BaseModel):
    cluster_id: int
    point_count: int
    avg_vitesse: float
    consensus_level: int
