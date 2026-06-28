from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.insar_point import InsarPoint
from app.schemas.insar import InsarPointResponse, InsarCluster
from app.core.insar_pipeline import execute_insar_pipeline

router = APIRouter(prefix="/api/insar", tags=["InSAR"])

@router.get("/{ouvrage_id}", response_model=List[InsarPointResponse])
async def get_insar_points(ouvrage_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InsarPoint).where(InsarPoint.ouvrage_id == ouvrage_id))
    points = result.scalars().all()
    
    response = []
    for pt in points:
        response.append(InsarPointResponse.model_validate(pt))
        
    return response

@router.get("/clusters", response_model=List[InsarCluster])
async def get_insar_clusters(db: AsyncSession = Depends(get_db)):
    # Mocking cluster aggregation for the stub
    # In real impl, we'd query and group by cluster_id
    return [
        InsarCluster(cluster_id=1, point_count=12, avg_vitesse=-6.5, consensus_level=3),
        InsarCluster(cluster_id=2, point_count=5, avg_vitesse=-3.2, consensus_level=1)
    ]

@router.get("/anomalies", response_model=List[InsarPointResponse])
async def get_insar_anomalies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InsarPoint).where(InsarPoint.consensus_level >= 2))
    points = result.scalars().all()
    
    response = []
    for pt in points:
        response.append(InsarPointResponse.model_validate(pt))
        
    return response

@router.post("/recompute")
async def recompute_insar_pipeline(db: AsyncSession = Depends(get_db)):
    # Real impl would fetch all points, call execute_insar_pipeline, and save back
    result = await db.execute(select(InsarPoint))
    points = result.scalars().all()
    
    # Convert ORM to dicts
    points_data = [
        {
            "id": p.id,
            "lat": p.lat,
            "lon": p.lon,
            "vitesse_los": p.vitesse_los,
            "cumul": p.cumul or 0
        }
        for p in points
    ]
    
    processed = execute_insar_pipeline(points_data)
    
    # Update back to DB
    # ... mapping updated fields back ...
    
    return {"status": "success", "message": "Pipeline InSAR exécuté avec succès."}
