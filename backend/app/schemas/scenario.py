from pydantic import BaseModel
from typing import List

class ScenarioRequest(BaseModel):
    scenario_id: str  # 'S1', 'S2', 'S3'
    budget: float

class ScenarioResponse(BaseModel):
    scenario: str
    status: str
    total_cost: float
    total_gain: float
    budget_used_pct: float
    selected_actions_ids: List[int]
