from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.inspection import Inspection
from app.models.observation import Observation
from app.exporters.pdf_report import generate_structure_sheet_pdf, generate_inspection_report_pdf
from app.exporters.excel_export import generate_maintenance_plan_excel
from app.models.action import Action

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/pdf/ouvrage/{id}")
def get_ouvrage_pdf(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Ouvrage).where(Ouvrage.id == id))
    ouvrage = result.scalar_one_or_none()
    
    if not ouvrage:
        raise HTTPException(status_code=404, detail="Ouvrage non trouvé")
        
    ouvrage_data = {
        "code": ouvrage.code,
        "nom": ouvrage.nom,
        "famille": ouvrage.famille,
        "classe": ouvrage.classe,
        "lat": ouvrage.lat,
        "lon": ouvrage.lon,
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
def get_inspection_pdf(id: int, db: Session = Depends(get_db)):
    result = db.execute(
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

@router.get("/excel/maintenance")
def get_maintenance_excel(db: Session = Depends(get_db)):
    result = db.execute(select(Action))
    actions = result.scalars().all()
    
    plan_data = {
        "Plan Global": [{"id": a.id, "ouvrage_id": a.ouvrage_id, "cout_estime": a.cout, "gain_risque": 0.5} for a in actions]
    }
    
    excel_buffer = generate_maintenance_plan_excel(plan_data)
    
    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=plan_maintenance.xlsx"}
    )
