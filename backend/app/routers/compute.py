from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict, Any

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.proba import Proba
from app.models.action import Action
from app.schemas.proba import ProbaResponse, ProbaMatrix
from app.schemas.scenario import ScenarioRequest, ScenarioResponse
from app.core.model_proba import compute_proba, classify_probability, recalculate_probabilities
from app.core.optimizer import run_budget_optimization

router = APIRouter(prefix="/api/compute", tags=["Compute"])


@router.post("/proba", response_model=Dict[str, str])
def recompute_probabilities(ouvrage_id: int = None, db: Session = Depends(get_db)):
    """
    Recompute probabilities for a single structure or all structures
    using the CDC dynamic logistic model (IAE + IAD).
    """
    query = select(Ouvrage)
    if ouvrage_id:
        query = query.where(Ouvrage.id == ouvrage_id)

    result = db.execute(query)
    ouvrages = result.scalars().all()

    if not ouvrages:
        raise HTTPException(status_code=404, detail="Ouvrage(s) non trouvé(s)")

    updated = 0
    for ouvrage in ouvrages:
        recalculate_probabilities(db, ouvrage.id)
        updated += 1

    return {
        "status": "success",
        "message": f"Probabilités recalculées pour {updated} ouvrage(s) via le modèle logistique CDC.",
    }


@router.get("/proba/matrix", response_model=List[ProbaMatrix])
def get_probability_matrix(db: Session = Depends(get_db)):
    result = db.execute(select(Proba))
    all_probas = result.scalars().all()

    # Group by ouvrage_id
    matrix_dict: Dict[int, Dict[str, Any]] = {}
    for p in all_probas:
        if p.ouvrage_id not in matrix_dict:
            matrix_dict[p.ouvrage_id] = {}
        matrix_dict[p.ouvrage_id][p.pathologie] = p.p_current

    return [ProbaMatrix(ouvrage_id=oid, probabilities=probs) for oid, probs in matrix_dict.items()]


@router.get("/proba/{ouvrage_id}", response_model=List[Any])
def get_probabilities(ouvrage_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Proba).where(Proba.ouvrage_id == ouvrage_id))
    probas = result.scalars().all()
    return [
        {"pathologie": r.pathologie, "p_current": r.p_current, "iae": r.iae, "iad": r.iad}
        for r in probas
    ]


@router.post("/optimize", response_model=ScenarioResponse)
def optimize_maintenance(req: ScenarioRequest, db: Session = Depends(get_db)):
    result = db.execute(select(Action))
    db_actions = result.scalars().all()

    # Filter out actions with missing cost
    valid_actions = [a for a in db_actions if a.cout is not None and a.cout > 0]

    actions_for_opt = []
    for a in valid_actions:
        # Risk gain derived from urgency level
        gain = 0.5
        if a.urgence == "0-3m":
            gain = 0.9
        elif a.urgence == "3-6m":
            gain = 0.7
        elif a.urgence == "6-12m":
            gain = 0.4

        actions_for_opt.append({
            "id": a.id,
            "ouvrage_id": a.ouvrage_id,
            "cost": a.cout,
            "risk_gain": gain,
            "is_class_a_critical": a.urgence == "0-3m",
            "is_class_a_high": a.urgence == "3-6m",
        })

    opt_result = run_budget_optimization(actions_for_opt, req.budget, req.scenario_id)

    return ScenarioResponse(
        scenario=opt_result["scenario"],
        status="Optimal" if opt_result["status"] == "Optimal" else "Infeasible",
        total_cost=opt_result["total_cost"],
        total_gain=opt_result["total_gain"],
        budget_used_pct=opt_result["budget_used_pct"],
        selected_actions_ids=opt_result["selected_actions"],
    )
