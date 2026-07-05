from fastapi import APIRouter
from pydantic import BaseModel
import math
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/api/area", tags=["Area Grid Analysis"])

# Constants
WAVELENGTH_MM = 55.465
TIF_PATH = Path(__file__).parent.parent.parent / 'data' / '20231021_20231208.geo.unw.tif'

def sigmoid(x: float) -> float:
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def compute_cell_probas(iad: float, iae: float) -> list:
    """Computes a generic risk profile for a grid cell using the logistic model."""
    probas = []
    
    # P12: Tassement / Soulèvement (Highly dependent on ground deformation IAD)
    p0_p12 = 0.15 # Baseline 15%
    seuil_p12 = 0.6
    k_p12 = 5.0
    z_p12 = k_p12 * ((iad * 0.8 + iae * 0.2) - seuil_p12)
    p_curr_p12 = p0_p12 + (1 - p0_p12) * sigmoid(z_p12)
    probas.append({"pathologie": "P12", "p_current": p_curr_p12 * 100, "iae": iae, "iad": iad})

    # P2: Corrosion (Highly dependent on environment IAE)
    p0_p2 = 0.25 # Baseline 25%
    seuil_p2 = 0.5
    k_p2 = 4.0
    z_p2 = k_p2 * ((iae * 0.9 + iad * 0.1) - seuil_p2)
    p_curr_p2 = p0_p2 + (1 - p0_p2) * sigmoid(z_p2)
    probas.append({"pathologie": "P2", "p_current": p_curr_p2 * 100, "iae": iae, "iad": iad})
    
    # P6: Affouillement (Mixed)
    p0_p6 = 0.10
    seuil_p6 = 0.7
    k_p6 = 4.5
    z_p6 = k_p6 * ((iad * 0.5 + iae * 0.5) - seuil_p6)
    p_curr_p6 = p0_p6 + (1 - p0_p6) * sigmoid(z_p6)
    probas.append({"pathologie": "P6", "p_current": p_curr_p6 * 100, "iae": iae, "iad": iad})

    return probas

def is_point_in_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

@router.get("/grid")
def get_area_grid(grid_size: int = 80):
    """
    Generates a GeoJSON feature collection of a dense grid covering Jorf Lasfar.
    """
    # Custom Jorf Lasfar Platform Polygon (Lon, Lat)
    polygon = [
        (-8.6285, 33.1625),
        (-8.636, 33.156),
        (-8.662, 33.148),
        (-8.654, 33.14),
        (-8.648, 33.133),
        (-8.638, 33.127),
        (-8.63, 33.123),
        (-8.627, 33.117),
        (-8.653, 33.107),
        (-8.643, 33.106),
        (-8.64, 33.108),
        (-8.6372, 33.106),
        (-8.636, 33.098),
        (-8.638, 33.091),
        (-8.634, 33.084),
        (-8.618, 33.078),
        (-8.605, 33.082),
        (-8.587, 33.086),
        (-8.582, 33.095),
        (-8.5969, 33.0989),
        (-8.605, 33.113),
        (-8.576, 33.093),
        (-8.563, 33.09),
        (-8.553, 33.094),
        (-8.551, 33.11),
        (-8.558, 33.131),
        (-8.578, 33.145),
        (-8.601, 33.148),
        (-8.612, 33.154),
        (-8.622, 33.159),
        (-8.6285, 33.1625)
    ]
    
    # Bounding box of the polygon
    min_lat = min(p[1] for p in polygon)
    max_lat = max(p[1] for p in polygon)
    min_lon = min(p[0] for p in polygon)
    max_lon = max(p[0] for p in polygon)
    
    features = []
    
    try:
        import rasterio
        has_raster = TIF_PATH.exists()
        
        # We will keep the TIFF open and query it for each cell
        src = rasterio.open(TIF_PATH) if has_raster else None
        band = 2 if src and src.count >= 2 else 1
        data = src.read(band) if src else None
        
        lat_step = (max_lat - min_lat) / grid_size
        lon_step = (max_lon - min_lon) / grid_size
        
        # Generic IAE (Assuming a recent NASA sync pulled high humidity/temp)
        # In a real scenario, this would query the latest EnvTimeseries or an spatial weather grid
        base_iae = 0.65 
        
        for i in range(grid_size):
            for j in range(grid_size):
                cell_lat = min_lat + i * lat_step
                cell_lon = min_lon + j * lon_step
                
                # Check if cell center is inside the boundary polygon
                if not is_point_in_polygon(cell_lon + lon_step/2, cell_lat + lat_step/2, polygon):
                    continue
                
                # Default IAD if no raster
                cell_iad = 0.1
                
                if src and data is not None:
                    try:
                        row, col = src.index(cell_lon, cell_lat)
                        if 0 <= row < src.height and 0 <= col < src.width:
                            phase_val = float(data[row, col])
                            disp_mm = float(- (WAVELENGTH_MM / (4 * math.pi)) * phase_val)
                            annual_v_los = float(disp_mm * (365 / 48))
                            if not math.isnan(disp_mm) and abs(disp_mm) < 1000:
                                cell_iad = float(min(abs(annual_v_los)/10.0, 1.0))
                    except Exception:
                        pass
                
                # Add a tiny bit of random spatial noise to IAE to simulate micro-climates/wind
                cell_iae = float(min(base_iae + (i % 3)*0.05 + (j % 2)*0.02, 1.0))
                
                probas = compute_cell_probas(cell_iad, cell_iae)
                max_risk = float(max(p["p_current"] for p in probas))
                
                # Cell Polygon Coordinates
                p1 = [cell_lon, cell_lat]
                p2 = [cell_lon + lon_step, cell_lat]
                p3 = [cell_lon + lon_step, cell_lat + lat_step]
                p4 = [cell_lon, cell_lat + lat_step]
                
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[p1, p2, p3, p4, p1]]
                    },
                    "properties": {
                        "lat": cell_lat + lat_step/2,
                        "lon": cell_lon + lon_step/2,
                        "iad": cell_iad,
                        "iae": cell_iae,
                        "max_risk": max_risk,
                        "probas": probas
                    }
                })
                
        if src:
            src.close()
            
    except Exception as e:
        print(f"Grid generation error: {e}")
        
    return {
        "type": "FeatureCollection",
        "features": features
    }
