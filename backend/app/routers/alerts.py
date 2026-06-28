from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.proba import Proba
from app.core.alerts import evaluate_alerts

router = APIRouter(prefix="/api", tags=["alerts"])

class AlertResponse(BaseModel):
    id: int
    ouvrage_code: str
    ouvrage_nom: str
    severity: str
    action: str
    source: str
    date: str

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    """
    Active alerts with priority. Uses real alert rule engine.
    """
    # Get all structures
    result = await db.execute(select(Ouvrage))
    ouvrages = result.scalars().all()
    
    # Get all probabilities
    proba_res = await db.execute(select(Proba))
    probas = proba_res.scalars().all()
    
    # Organize probabilities by ouvrage_id
    proba_map = {}
    for p in probas:
        if p.ouvrage_id not in proba_map:
            proba_map[p.ouvrage_id] = {}
        proba_map[p.ouvrage_id][p.pathologie_code] = p.probability
        
    generated_alerts = []
    alert_id = 1
    
    for ouv in ouvrages:
        ouvrage_data = {
            "classe": ouv.classe,
            "iad": ouv.iad or 0.0,
            "iae": ouv.iae or 0.0,
            "etat_global": "E0" # would be derived from last inspection
        }
        proba_data = proba_map.get(ouv.id, {})
        insar_data = {"consensus_max": 2 if ouv.iad and ouv.iad > 0.6 else 0} # Mock consensus
        env_data = {}
        
        ouv_alerts = evaluate_alerts(ouvrage_data, proba_data, insar_data, env_data)
        
        for alert in ouv_alerts:
            generated_alerts.append(AlertResponse(
                id=alert_id,
                ouvrage_code=ouv.code,
                ouvrage_nom=ouv.nom,
                severity=alert['level'],
                action=alert['message'],
                source="Moteur de règles",
                date=datetime.now().strftime("%Y-%m-%d")
            ))
            alert_id += 1
            
    # If no alerts found (e.g. no data yet), return a generic message or keep empty
    # We will return the list
    return generated_alerts
