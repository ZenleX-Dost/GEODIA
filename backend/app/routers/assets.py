"""
Asset (Ouvrage) API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.proba import Proba
from app.models.inspection import Inspection
from app.models.insar_point import InsarPoint
from app.schemas.ouvrage import (
    OuvrageResponse,
    OuvrageGeoJSON,
    OuvrageGeoJSONFeature,
    OuvrageGeoJSONProperties,
    KPISummary,
)

router = APIRouter(prefix="/api", tags=["assets"])


@router.get("/assets", response_model=list[OuvrageResponse])
def list_assets(
    classe: Optional[str] = Query(None, description="Filter by classe A/B/C/D"),
    famille: Optional[str] = Query(None, description="Filter by famille"),
    search: Optional[str] = Query(None, description="Search by name or code"),
    db: Session = Depends(get_db),
):
    """List all structures with optional filters."""
    query = db.query(Ouvrage)
    if classe:
        query = query.filter(Ouvrage.classe == classe.upper())
    if famille:
        query = query.filter(Ouvrage.famille == famille)
    if search:
        query = query.filter(
            (Ouvrage.nom.ilike(f"%{search}%"))
            | (Ouvrage.code.ilike(f"%{search}%"))
        )
    return query.order_by(Ouvrage.ipd.desc().nullslast()).all()


@router.get("/assets/geojson", response_model=OuvrageGeoJSON)
def list_assets_geojson(
    classe: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Return all structures as GeoJSON FeatureCollection."""
    query = db.query(Ouvrage)
    if classe:
        query = query.filter(Ouvrage.classe == classe.upper())
    ouvrages = query.all()

    features = []
    for o in ouvrages:
        features.append(
            OuvrageGeoJSONFeature(
                geometry={
                    "type": "Point",
                    "coordinates": [o.lon, o.lat],
                },
                properties=OuvrageGeoJSONProperties(
                    id=o.id,
                    code=o.code,
                    nom=o.nom,
                    famille=o.famille,
                    classe=o.classe,
                    ipd=o.ipd,
                    ied=o.ied,
                    exposition=o.exposition,
                ),
            )
        )
    return OuvrageGeoJSON(features=features)


@router.get("/assets/{asset_id}", response_model=OuvrageResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """Get full detail for a single structure."""
    ouvrage = db.query(Ouvrage).filter(Ouvrage.id == asset_id).first()
    if not ouvrage:
        raise HTTPException(status_code=404, detail="Ouvrage non trouvé")
    return ouvrage


@router.get("/kpis", response_model=KPISummary)
def get_kpis(db: Session = Depends(get_db)):
    """Cockpit KPI summary."""
    total = db.query(Ouvrage).count()
    classe_a = db.query(Ouvrage).filter(Ouvrage.classe == "A").count()

    # InSAR alerts: count InSAR points with anomalies (IAD > 0.6)
    alertes_insar = db.query(InsarPoint).filter(
        InsarPoint.iad.isnot(None),
        InsarPoint.iad > 0.6,
    ).count()

    # Pending inspections: structures never inspected or inspected > 6 months ago
    inspected_ids = db.query(Inspection.ouvrage_id).distinct().all()
    inspected_set = {r[0] for r in inspected_ids}
    all_ids = {r[0] for r in db.query(Ouvrage.id).all()}
    inspections_pending = len(all_ids - inspected_set)

    # Prevention index: avg IPD of all structures (normalized to /100)
    from sqlalchemy import func
    avg_ipd = db.query(func.avg(Ouvrage.ipd)).scalar() or 0

    # Potential savings: placeholder based on class distribution
    # In V1 with simulated data, we estimate savings as 30% of reference budget
    economie = 6_600_000 * 0.30  # 30% of 5-year reference budget

    return KPISummary(
        total_ouvrages=total,
        classe_a_count=classe_a,
        alertes_insar=alertes_insar,
        inspections_pending=inspections_pending,
        indice_prevention=round(avg_ipd, 1),
        economie_potentielle=economie,
    )
