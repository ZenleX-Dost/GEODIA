from fastapi import APIRouter, Depends, UploadFile, File
from typing import Dict
import os

router = APIRouter(prefix="/api/imports", tags=["Imports"])

@router.post("/env", response_model=Dict[str, str])
async def import_environmental_data(ouvrage_id: int):
    """
    Trigger environmental data import for a specific structure.
    Currently uses simulated data.
    """
    return {
        "status": "success",
        "message": f"Données environnementales simulées importées avec succès pour l'ouvrage {ouvrage_id}."
    }

@router.post("/upload", response_model=Dict[str, str])
async def upload_data_file(file: UploadFile = File(...), type: str = "insar"):
    """
    Upload CSV/Excel file for data integration (InSAR, Climat, Pathologies, etc.).
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {
        "status": "success",
        "message": f"Fichier {file.filename} ({type}) uploadé avec succès et prêt pour l'intégration.",
        "filename": file.filename
    }
