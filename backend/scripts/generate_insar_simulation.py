import sys
from pathlib import Path
import random
from datetime import date

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.ouvrage import Ouvrage
from app.models.insar_point import InsarPoint

def generate_insar():
    db = SessionLocal()
    try:
        ouvrages = db.query(Ouvrage).all()
        if not ouvrages:
            print("No ouvrages found in DB. Run seed_db.py first.")
            return

        # Clear existing InSAR points
        db.query(InsarPoint).delete()
        
        count = 0
        for ouv in ouvrages:
            # Determine base velocity based on ouvrage.
            # E.g., make Ouvrage 3 (Bassin tranquillisation) and 4 (Canal de rejet) subside a bit
            base_velocity = 0.0
            if ouv.id in [3, 4, 12]:  
                base_velocity = -4.5  # subsidence of 4.5 mm/year
            elif ouv.classe == "A":
                base_velocity = -1.0
            
            # Generate 20-50 points per ouvrage
            num_points = random.randint(20, 50)
            for _ in range(num_points):
                # Small random offset for lat/lon (approx 10-50 meters)
                lat_offset = random.uniform(-0.0005, 0.0005)
                lon_offset = random.uniform(-0.0005, 0.0005)
                
                # Add some noise to velocity
                v_los = base_velocity + random.uniform(-1.5, 1.5)
                
                pt = InsarPoint(
                    ouvrage_id=ouv.id,
                    lat=ouv.lat + lat_offset,
                    lon=ouv.lon + lon_offset,
                    date_start=date(2024, 1, 1),
                    date_end=date(2026, 1, 1),
                    vitesse_los=round(v_los, 2),
                    cumul=round(v_los * 2, 2),
                    acceleration=round(random.uniform(-0.5, 0.5), 2),
                    r2=round(random.uniform(0.85, 0.99), 2),
                    cluster_id=ouv.id,  # just group by ouvrage for simulation
                    iad=round(min(abs(v_los) / 5.0, 1.0), 2),  # Simulated IAD
                    source="Simulation ASF Vertex",
                    is_simulated=True
                )
                db.add(pt)
                count += 1
                
        db.commit()
        print(f"[OK] Generated {count} simulated InSAR points across {len(ouvrages)} structures.")
        
    finally:
        db.close()

if __name__ == "__main__":
    generate_insar()
