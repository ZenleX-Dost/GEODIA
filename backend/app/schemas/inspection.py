"""
Pydantic schemas for Inspections and Observations.
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional


# -------------------------------------------------------------------
# Observations
# -------------------------------------------------------------------

class ObservationBase(BaseModel):
    pathologie_code: str
    zone: str
    gravite: int = Field(..., ge=0, le=3, description="0=Aucune, 1=Faible, 2=Moyenne, 3=Forte")
    etendue_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    preuves: Optional[str] = None
    photo_url: Optional[str] = None


class ObservationCreate(ObservationBase):
    pass


class ObservationResponse(ObservationBase):
    id: int
    inspection_id: int
    pathologie_nom: Optional[str] = None # Filled by joining with Pathologie

    class Config:
        from_attributes = True


# -------------------------------------------------------------------
# Inspections
# -------------------------------------------------------------------

class InspectionBase(BaseModel):
    ouvrage_id: int
    date_inspection: date
    inspecteur: str
    etat_global: str = Field(..., description="E0, E1, E2, E3")
    notes: Optional[str] = None


class InspectionCreate(InspectionBase):
    observations: List[ObservationCreate] = []


class InspectionUpdate(BaseModel):
    etat_global: Optional[str] = None
    notes: Optional[str] = None
    statut: Optional[str] = None


class InspectionResponse(InspectionBase):
    id: int
    statut: str
    created_at: datetime
    observations: List[ObservationResponse] = []
    
    # Extra fields for list views
    ouvrage_code: Optional[str] = None
    ouvrage_nom: Optional[str] = None

    class Config:
        from_attributes = True
