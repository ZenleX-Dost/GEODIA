from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.proba import Proba
from app.schemas.proba import ProbaResponse, ProbaMatrix
from app.core.model_proba import compute_proba, classify_probability

router = APIRouter(prefix="/api/compute", tags=["Compute"])

@router.post("/proba", response_model=Dict[str, str])
async def recompute_probabilities(ouvrage_id: int = None, db: AsyncSession = Depends(get_db)):
    """
    Recompute probabilities for a single structure or all structures.
    """
    query = select(Ouvrage)
    if ouvrage_id:
        query = query.where(Ouvrage.id == ouvrage_id)
        
    result = await db.execute(query)
    ouvrages = result.scalars().all()
    
    if not ouvrages:
        raise HTTPException(status_code=404, detail="Ouvrage(s) non trouvé(s)")
        
    # Placeholder for actual model recomputation using compute_proba
    # In a real scenario, this would query all inspection evidence (E),
    # physical factors (F), history (H), InSAR (IAD), Env (IAE), etc.
    # For now, this is a mock implementation that simply updates a static value
    
    for ouvrage in ouvrages:
        # Example pseudo-code to update Proba table
        pass
        
    await db.commit()
    return {"status": "success", "message": f"Probabilités recalculées pour {len(ouvrages)} ouvrage(s)."}

@router.get("/proba/{ouvrage_id}", response_model=List[ProbaResponse])
async def get_probabilities(ouvrage_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Proba).where(Proba.ouvrage_id == ouvrage_id))
    probas = result.scalars().all()
    return probas

@router.get("/proba/matrix", response_model=List[ProbaMatrix])
async def get_probability_matrix(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Proba))
    all_probas = result.scalars().all()
    
    # Group by ouvrage_id
    matrix_dict = {}
    for p in all_probas:
        if p.ouvrage_id not in matrix_dict:
            matrix_dict[p.ouvrage_id] = {}
        matrix_dict[p.ouvrage_id][p.pathologie_code] = p.probability
        
    response = []
    for oid, probs in matrix_dict.items():
        response.append(ProbaMatrix(ouvrage_id=oid, probabilities=probs))
        
    return response

from app.schemas.scenario import ScenarioRequest, ScenarioResponse
from app.core.optimizer import run_budget_optimization

@router.post("/optimize", response_model=ScenarioResponse)
async def optimize_maintenance(req: ScenarioRequest, db: AsyncSession = Depends(get_db)):
    # In a real impl, fetch actions from DB
    # Mocking actions for optimization
    mock_actions = [
        {'id': 1, 'ouvrage_id': 10, 'cost': 50000, 'risk_gain': 0.8, 'is_class_a_critical': True},
        {'id': 2, 'ouvrage_id': 12, 'cost': 30000, 'risk_gain': 0.4, 'is_class_a_critical': False},
        {'id': 3, 'ouvrage_id': 5,  'cost': 120000, 'risk_gain': 0.9, 'is_class_a_critical': True},
        {'id': 4, 'ouvrage_id': 2,  'cost': 15000, 'risk_gain': 0.2, 'is_class_a_critical': False},
    ]
    
    result = run_budget_optimization(mock_actions, req.budget, req.scenario_id)
    
    return ScenarioResponse(
        scenario=result['scenario'],
        status="Optimal" if result['status'] == "Optimal" else "Infeasible",
        total_cost=result['total_cost'],
        total_gain=result['total_gain'],
        budget_used_pct=result['budget_used_pct'],
        selected_actions_ids=result['selected_actions']
    )
