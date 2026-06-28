from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.inspection import Inspection
from app.models.observation import Observation
from app.exporters.pdf_report import generate_structure_sheet_pdf, generate_inspection_report_pdf

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/pdf/ouvrage/{id}")
async def get_ouvrage_pdf(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ouvrage).where(Ouvrage.id == id))
    ouvrage = result.scalar_one_or_none()
    
    if not ouvrage:
        raise HTTPException(status_code=404, detail="Ouvrage non trouvé")
        
    ouvrage_data = {
        "code": ouvrage.code,
        "nom": ouvrage.nom,
        "famille": ouvrage.famille,
        "classe": ouvrage.classe,
        "gps_lat": ouvrage.gps_lat,
        "gps_long": ouvrage.gps_long,
        "icf": ouvrage.icf,
        "ivp": ouvrage.ivp,
        "ipd": ouvrage.ipd,
        "ied": ouvrage.ied
    }
    
    pdf_buffer = generate_structure_sheet_pdf(ouvrage.id, ouvrage_data)
    
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=fiche_ouvrage_{ouvrage.code}.pdf"}
    )

@router.get("/pdf/inspection/{id}")
async def get_inspection_pdf(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Inspection).options(selectinload(Inspection.observations)).where(Inspection.id == id)
    )
    inspection = result.scalar_one_or_none()
    
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection non trouvée")
        
    inspection_data = {
        "date": inspection.date.strftime("%Y-%m-%d"),
        "inspecteur": inspection.inspecteur,
        "etat": inspection.etat,
        "commentaire": inspection.commentaire
    }
    
    observations = [
        {
            "zone": obs.zone,
            "pathologie_code": obs.pathologie_code,
            "gravite": obs.gravite,
            "etendue_pct": obs.etendue_pct
        } for obs in inspection.observations
    ]
    
    pdf_buffer = generate_inspection_report_pdf(inspection.id, inspection_data, observations)
    
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=rapport_inspection_{inspection.id}.pdf"}
    )
