from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class InsarPointBase(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    vitesse_los: Optional[float] = None
    cumul: Optional[float] = None


class InsarPointResponse(InsarPointBase):
    id: int
    ouvrage_id: Optional[int] = None
    # Computed indices & pipeline outputs
    iad: Optional[float] = None
    r2: Optional[float] = None
    acceleration: Optional[float] = None
    cluster_id: Optional[int] = None
    consensus_level: Optional[int] = None
    is_anomaly_iso: Optional[bool] = None
    # Metadata
    date_start: Optional[date] = None
    date_end: Optional[date] = None
    source: Optional[str] = None
    is_simulated: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class InsarCluster(BaseModel):
    cluster_id: int
    point_count: int
    avg_vitesse: float
    consensus_level: int

