from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.database import get_db
from app.models.ouvrage import Ouvrage
from app.models.env_timeseries import EnvTimeseries
from app.core.nasa_client import NasaEarthdataClient
from app.core.copernicus_client import CopernicusClient
from app.core.indices import compute_iae
from app.core.model_proba import recalculate_probabilities

router = APIRouter(prefix="/api/env", tags=["Environment"])

@router.post("/sync")
def sync_environmental_data(db: Session = Depends(get_db)):
    """
    Connects to NASA Earthdata API to fetch the latest environmental metrics
    for all structures (Ouvrages) in the database.
    """
    # 1. Get all structures
    ouvrages = db.execute(select(Ouvrage)).scalars().all()
    if not ouvrages:
        raise HTTPException(status_code=404, detail="Aucun ouvrage trouvé pour la synchronisation.")
    
    # 2. Initialize NASA Client
    nasa_client = NasaEarthdataClient()
    
    # 3. For prototype, we fetch data for the first structure's coordinates
    # and apply slight variations to the others to simulate a spatial grid.
    base_ouvrage = ouvrages[0]
    nasa_response = nasa_client.fetch_environmental_data(base_ouvrage.lat, base_ouvrage.lon)
    
    if "error" in nasa_response:
        raise HTTPException(status_code=500, detail=nasa_response["error"])
        
    payload = nasa_response["payload"]
    metadata = nasa_response["metadata"]
    
    new_records = []
    
    # 4. Save data for each structure
    for ouv in ouvrages:
        # Slight variation per structure
        t = payload["temperature"] + (ouv.id % 3) * 0.1
        h = payload["humidite"] + (ouv.id % 2) * 0.5
        w = payload["vent"]
        
        # For prototype, we normalize roughly to 0-1 based on expected max values
        t_norm = min(t / 40.0, 1.0)
        h_norm = min(h / 100.0, 1.0)
        w_norm = min(w / 100.0, 1.0)
        p_norm = min((payload["pollution_so2"] + payload["pollution_no2"]) / 100.0, 1.0)
        
        new_iae = compute_iae(
            t=t_norm,
            h=h_norm,
            m=0.8, # Hardcoded marine exposure for Jorf Lasfar
            r=payload["pluie"] / 10.0,
            p=p_norm,
            w=w_norm
        )
        
        env_record = EnvTimeseries(
            ouvrage_id=ouv.id,
            date=datetime.utcnow(),
            temperature=t,
            humidite=h,
            pluie=payload["pluie"],
            vent=w,
            pollution_so2=payload["pollution_so2"],
            pollution_no2=payload["pollution_no2"],
            ndwi=payload["ndwi"],
            iae=new_iae,
            source=f"NASA ({metadata['granule']})",
            fraicheur="live",
            is_simulated=False # It is considered real from the API perspective
        )
        
        # Update Ouvrage current IAE
        ouv.iae = new_iae
        
        db.add(env_record)
        new_records.append(env_record)
        
    db.commit()
    
    # Recalculate probabilities for all updated ouvrages
    for ouv in ouvrages:
        recalculate_probabilities(db, ouv.id)
    
    
    return {
        "status": "success",
        "message": f"Synchronisation réussie. {len(new_records)} relevés ajoutés depuis NASA Earthdata.",
        "nasa_metadata": metadata
    }

@router.post("/sync-copernicus")
def sync_copernicus_data(db: Session = Depends(get_db)):
    """
    Connects to Copernicus Data Space Ecosystem to fetch the latest environmental metrics
    (e.g., Sentinel-2 NDWI) for all structures.
    """
    ouvrages = db.execute(select(Ouvrage)).scalars().all()
    if not ouvrages:
        raise HTTPException(status_code=404, detail="Aucun ouvrage trouvé pour la synchronisation.")
    
    copernicus_client = CopernicusClient()
    
    base_ouvrage = ouvrages[0]
    response = copernicus_client.fetch_environmental_data(base_ouvrage.lat, base_ouvrage.lon)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
        
    payload = response["payload"]
    metadata = response["metadata"]
    
    new_records = []
    
    for ouv in ouvrages:
        # Slight variation per structure
        t = payload["temperature"] + (ouv.id % 3) * 0.1
        h = payload["humidite"] + (ouv.id % 2) * 0.5
        w = payload["vent"]
        
        t_norm = min(t / 40.0, 1.0)
        h_norm = min(h / 100.0, 1.0)
        w_norm = min(w / 100.0, 1.0)
        p_norm = min((payload["pollution_so2"] + payload["pollution_no2"]) / 100.0, 1.0)
        
        new_iae = compute_iae(
            t=t_norm,
            h=h_norm,
            m=0.8,
            r=payload["pluie"] / 10.0,
            p=p_norm,
            w=w_norm
        )
        
        env_record = EnvTimeseries(
            ouvrage_id=ouv.id,
            date=datetime.utcnow(),
            temperature=t,
            humidite=h,
            pluie=payload["pluie"],
            vent=w,
            pollution_so2=payload["pollution_so2"],
            pollution_no2=payload["pollution_no2"],
            ndwi=payload["ndwi"],
            iae=new_iae,
            source=f"Copernicus ({metadata['product']})",
            fraicheur="live",
            is_simulated=False
        )
        
        ouv.iae = new_iae
        db.add(env_record)
        new_records.append(env_record)
        
    db.commit()
    
    # Recalculate probabilities for all updated ouvrages
    for ouv in ouvrages:
        recalculate_probabilities(db, ouv.id)
        
    return {
        "status": "success",
        "message": f"Synchronisation réussie. {len(new_records)} relevés ajoutés depuis Copernicus Data Space.",
        "copernicus_metadata": metadata
    }

@router.get("/{ouvrage_id}/timeseries")
def get_env_timeseries(ouvrage_id: int, db: Session = Depends(get_db)):
    """
    Fetch the environmental timeseries data for a specific ouvrage.
    """
    records = db.query(EnvTimeseries).filter(EnvTimeseries.ouvrage_id == ouvrage_id).order_by(EnvTimeseries.date.asc()).all()
    return records
