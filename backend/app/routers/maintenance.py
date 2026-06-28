from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.action import Action
from app.schemas.maintenance import ActionResponse, MaintenancePlan

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])

@router.get("/plan", response_model=MaintenancePlan)
async def get_maintenance_plan(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Action))
    actions = result.scalars().all()
    
    plan = {
        "actions_0_3m": [],
        "actions_3_6m": [],
        "actions_6_12m": [],
        "actions_12m_plus": []
    }
    
    for a in actions:
        action_resp = ActionResponse.model_validate(a)
        # Mocking logic for horizons based on some criteria
        # In real impl, horizon would be a field or calculated
        # For stub, we'll randomly assign based on id
        if a.id % 4 == 0:
            plan["actions_0_3m"].append(action_resp)
        elif a.id % 4 == 1:
            plan["actions_3_6m"].append(action_resp)
        elif a.id % 4 == 2:
            plan["actions_6_12m"].append(action_resp)
        else:
            plan["actions_12m_plus"].append(action_resp)
            
    return plan

@router.get("/actions", response_model=List[ActionResponse])
async def get_all_actions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Action))
    actions = result.scalars().all()
    return [ActionResponse.model_validate(a) for a in actions]
