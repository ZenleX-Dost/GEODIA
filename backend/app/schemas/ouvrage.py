"""
Pydantic schemas for Ouvrage (structure/asset) endpoints.
"""
from datetime import datetime
from pydantic import BaseModel, Field


class OuvrageBase(BaseModel):
    code: str
    nom: str
    famille: str
    lat: float
    lon: float
    classe: str
    icf: float | None = None
    ivp: float | None = None
    ipd: float | None = None
    ied: float | None = None
    exposition: str | None = None


class OuvrageCreate(OuvrageBase):
    pass


class OuvrageResponse(OuvrageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OuvrageGeoJSONProperties(BaseModel):
    id: int
    code: str
    nom: str
    famille: str
    classe: str
    ipd: float | None = None
    ied: float | None = None
    exposition: str | None = None


class OuvrageGeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: OuvrageGeoJSONProperties


class OuvrageGeoJSON(BaseModel):
    type: str = "FeatureCollection"
    features: list[OuvrageGeoJSONFeature]


class KPISummary(BaseModel):
    """Cockpit KPI summary."""
    total_ouvrages: int
    classe_a_count: int
    alertes_insar: int
    inspections_pending: int
    indice_prevention: float = Field(description="Global prevention score /100")
    economie_potentielle: float = Field(description="Budget savings vs no-action (DH)")
