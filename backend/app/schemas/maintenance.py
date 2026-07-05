from pydantic import BaseModel
from typing import List

class ActionBase(BaseModel):
    ouvrage_id: int
    pathologie: str | None = None
    type_action: str | None = None
    cout: float | None = None
    duree_jours: int | None = None
    urgence: str | None = None
    statut: str | None = None
    declencheur: str | None = None

class ActionResponse(ActionBase):
    id: int
    
    class Config:
        from_attributes = True

class MaintenancePlan(BaseModel):
    actions_0_3m: List[ActionResponse]
    actions_3_6m: List[ActionResponse]
    actions_6_12m: List[ActionResponse]
    actions_12m_plus: List[ActionResponse]
