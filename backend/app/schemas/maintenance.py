from pydantic import BaseModel
from typing import List

class ActionBase(BaseModel):
    ouvrage_id: int
    nom: str
    description: str
    horizon: str  # 0-3m, 3-6m, 6-12m, >12m
    cout_estime: float
    gain_risque: float
    is_class_a_critical: bool = False

class ActionResponse(ActionBase):
    id: int
    
    class Config:
        from_attributes = True

class MaintenancePlan(BaseModel):
    actions_0_3m: List[ActionResponse]
    actions_3_6m: List[ActionResponse]
    actions_6_12m: List[ActionResponse]
    actions_12m_plus: List[ActionResponse]
