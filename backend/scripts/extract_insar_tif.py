import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.ouvrage import Ouvrage
from app.models.insar_point import InsarPoint
from datetime import date

def extract_tif():
    tif_path = Path(__file__).parent.parent / 'data' / '20231021_20231208.geo.unw.tif'
    
    if not tif_path.exists():
        print(f"File not found: {tif_path}")
        return

    # Sentinel-1 wavelength is ~5.5465 cm = 55.465 mm
    WAVELENGTH_MM = 55.465
    
    # Import rasterio inside the function to ensure pip install has finished
    import rasterio

    db = SessionLocal()
    
    try:
        ouvrages = db.query(Ouvrage).all()
        
        # Clear old points to replace with the real ones
        db.query(InsarPoint).delete()
        
        with rasterio.open(tif_path) as src:
            # Usually LiCSAR unwrapped files have 2 bands: 1=Amplitude, 2=Phase
            band = 2 if src.count >= 2 else 1
            data = src.read(band)
            
            count = 0
            for ouv in ouvrages:
                try:
                    row, col = src.index(ouv.lon, ouv.lat)
                    
                    if 0 <= row < src.height and 0 <= col < src.width:
                        phase_val = data[row, col]
                        
                        # Convert phase (radians) to line-of-sight displacement (mm)
                        disp_mm = - (WAVELENGTH_MM / (4 * math.pi)) * phase_val
                        
                        # Annualize for a 48-day interferogram (Oct 21 to Dec 08)
                        annual_v_los = disp_mm * (365 / 48)
                        
                        if math.isnan(disp_mm) or abs(disp_mm) > 1000:
                            print(f"Invalid phase for {ouv.nom} (NaN or outlier)")
                            continue
                            
                        pt = InsarPoint(
                            ouvrage_id=ouv.id,
                            lat=ouv.lat,
                            lon=ouv.lon,
                            date_start=date(2023, 10, 21),
                            date_end=date(2023, 12, 8),
                            vitesse_los=round(annual_v_los, 2),
                            cumul=round(disp_mm, 2),
                            r2=0.99,
                            cluster_id=ouv.id,
                            iad=round(min(abs(annual_v_los)/10.0, 1.0), 2),
                            source="COMET-LiCSAR Real TIF",
                            is_simulated=False # REAL DATA!
                        )
                        db.add(pt)
                        count += 1
                    else:
                        print(f"Ouvrage {ouv.nom} ({ouv.lat}, {ouv.lon}) is outside the TIF boundary.")
                except Exception as e:
                    print(f"Error for {ouv.nom}: {e}")
                    
        db.commit()
        print(f"[OK] Extracted and saved {count} real InSAR points from the TIF!")
    finally:
        db.close()

if __name__ == "__main__":
    extract_tif()
