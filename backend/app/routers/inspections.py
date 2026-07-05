"""
Inspections API — fully synchronous (matches the sync SQLAlchemy engine).
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
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
    ObservationResponse,
)
from app.config import settings

router = APIRouter(prefix="/api/inspections", tags=["Inspections"])


@router.post("", response_model=InspectionResponse)
def create_inspection(inspection_in: InspectionCreate, db: Session = Depends(get_db)):
    """Create a new inspection with optional observations."""
    new_inspection = Inspection(
        ouvrage_id=inspection_in.ouvrage_id,
        date=inspection_in.date_inspection,
        inspecteur=inspection_in.inspecteur,
        etat=inspection_in.etat_global,
        commentaire=inspection_in.notes,
        validation=False,
        photos="[]",
    )
    db.add(new_inspection)
    db.flush()  # populate new_inspection.id before adding observations

    for obs_in in inspection_in.observations:
        new_obs = Observation(
            inspection_id=new_inspection.id,
            pathologie=obs_in.pathologie_code,
            zone=obs_in.zone,
            gravite=obs_in.gravite,
            etendue=obs_in.etendue_pct,
            preuve=obs_in.preuves,
        )
        db.add(new_obs)

    db.commit()
    db.refresh(new_inspection)

    return InspectionResponse(
        id=new_inspection.id,
        ouvrage_id=new_inspection.ouvrage_id,
        date_inspection=new_inspection.date,
        inspecteur=new_inspection.inspecteur,
        etat_global=new_inspection.etat,
        notes=new_inspection.commentaire,
        statut="Validée" if new_inspection.validation else "En attente",
        created_at=new_inspection.created_at,
        observations=[],
    )


@router.get("", response_model=List[InspectionResponse])
def list_inspections(ouvrage_id: Optional[int] = None, db: Session = Depends(get_db)):
    """List all inspections, optionally filtered by ouvrage."""
    query = select(Inspection)
    if ouvrage_id:
        query = query.where(Inspection.ouvrage_id == ouvrage_id)

    inspections = db.execute(query).scalars().all()

    return [
        InspectionResponse(
            id=insp.id,
            ouvrage_id=insp.ouvrage_id,
            date_inspection=insp.date,
            inspecteur=insp.inspecteur,
            etat_global=insp.etat,
            notes=insp.commentaire,
            statut="Validée" if insp.validation else "En attente",
            created_at=insp.created_at,
            observations=[],
        )
        for insp in inspections
    ]


@router.get("/{id}", response_model=InspectionResponse)
def get_inspection(id: int, db: Session = Depends(get_db)):
    """Get a single inspection by ID."""
    insp = db.execute(select(Inspection).where(Inspection.id == id)).scalar_one_or_none()
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
        observations=[],
    )


@router.post("/{id}/photos")
def upload_inspection_photo(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and attach a photo to an existing inspection."""
    insp = db.execute(select(Inspection).where(Inspection.id == id)).scalar_one_or_none()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection non trouvée")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(str(settings.UPLOAD_DIR), file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    photos: list = []
    if insp.photos:
        try:
            photos = json.loads(insp.photos)
        except json.JSONDecodeError:
            photos = []

    photos.append(file_path)
    insp.photos = json.dumps(photos)
    db.commit()

    return {"filename": file.filename, "path": file_path}


@router.patch("/{id}/validate")
def validate_inspection(id: int, db: Session = Depends(get_db)):
    """Mark an inspection as validated."""
    insp = db.execute(select(Inspection).where(Inspection.id == id)).scalar_one_or_none()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection non trouvée")

    insp.validation = True
    db.commit()
    return {"status": "success", "message": "Inspection validée"}
