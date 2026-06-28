from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import shutil
import os
import json

from app.database import get_db
from app.models.inspection import Inspection
from app.models.observation import Observation
from app.models.ouvrage import Ouvrage
from app.schemas.inspection import (
    InspectionCreate,
    InspectionResponse,
    InspectionUpdate,
    ObservationCreate,
    ObservationResponse
)
from app.config import settings

router = APIRouter(prefix="/api/inspections", tags=["Inspections"])

@router.post("", response_model=InspectionResponse)
async def create_inspection(inspection_in: InspectionCreate, db: AsyncSession = Depends(get_db)):
    # Create the inspection model
    new_inspection = Inspection(
        ouvrage_id=inspection_in.ouvrage_id,
        date=inspection_in.date_inspection,
        inspecteur=inspection_in.inspecteur,
        etat=inspection_in.etat_global,
        commentaire=inspection_in.notes,
        validation=False,
        photos="[]"
    )
    
    db.add(new_inspection)
    await db.flush() # To get the new_inspection.id
    
    # Add observations
    for obs_in in inspection_in.observations:
        new_obs = Observation(
            inspection_id=new_inspection.id,
            pathologie_code=obs_in.pathologie_code,
            zone=obs_in.zone,
            gravite=obs_in.gravite,
            etendue_pct=obs_in.etendue_pct,
            preuves=obs_in.preuves,
            photo_url=obs_in.photo_url
        )
        db.add(new_obs)
        
    await db.commit()
    await db.refresh(new_inspection)
    
    # Transform model back to schema response
    # For a real implementation, we would want to join with Ouvrage to get nom/code
    # but returning basic info for now.
    return InspectionResponse(
        id=new_inspection.id,
        ouvrage_id=new_inspection.ouvrage_id,
        date_inspection=new_inspection.date,
        inspecteur=new_inspection.inspecteur,
        etat_global=new_inspection.etat,
        notes=new_inspection.commentaire,
        statut="Validée" if new_inspection.validation else "En attente",
        created_at=new_inspection.created_at,
        observations=[] # To keep simple for now
    )

@router.get("", response_model=List[InspectionResponse])
async def list_inspections(ouvrage_id: int = None, db: AsyncSession = Depends(get_db)):
    query = select(Inspection)
    if ouvrage_id:
        query = query.where(Inspection.ouvrage_id == ouvrage_id)
        
    result = await db.execute(query)
    inspections = result.scalars().all()
    
    response = []
    for insp in inspections:
        response.append(InspectionResponse(
            id=insp.id,
            ouvrage_id=insp.ouvrage_id,
            date_inspection=insp.date,
            inspecteur=insp.inspecteur,
            etat_global=insp.etat,
            notes=insp.commentaire,
            statut="Validée" if insp.validation else "En attente",
            created_at=insp.created_at,
            observations=[]
        ))
    return response

@router.get("/{id}", response_model=InspectionResponse)
async def get_inspection(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Inspection).where(Inspection.id == id))
    insp = result.scalar_one_or_none()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection non trouvée")
        
    return InspectionResponse(
        id=insp.id,
        ouvrage_id=insp.ouvrage_id,
        date_inspection=insp.date,
        inspecteur=insp.inspecteur,
        etat_global=insp.etat,
        notes=insp.commentaire,
        statut="Validée" if insp.validation else "En attente",
        created_at=insp.created_at,
        observations=[]
    )

@router.post("/{id}/photos")
async def upload_inspection_photo(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Inspection).where(Inspection.id == id))
    insp = result.scalar_one_or_none()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection non trouvée")
        
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    photos = []
    if insp.photos:
        try:
            photos = json.loads(insp.photos)
        except:
            pass
            
    photos.append(file_path)
    insp.photos = json.dumps(photos)
    
    await db.commit()
    return {"filename": file.filename, "path": file_path}

@router.patch("/{id}/validate")
async def validate_inspection(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Inspection).where(Inspection.id == id))
    insp = result.scalar_one_or_none()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection non trouvée")
        
    insp.validation = True
    await db.commit()
    return {"status": "success", "message": "Inspection validée"}
