"""
Seed the database with initial data from CSV files.
Usage: python -m scripts.seed_db
"""
import csv
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import engine, SessionLocal, Base
from app.models import Ouvrage, Pathologie, Proba, Action


def load_csv(filepath: Path) -> list[dict]:
    """Load a CSV file and return list of row dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def seed_ouvrages(db):
    """Seed the ouvrages table."""
    filepath = settings.SEED_DIR / "ouvrages.csv"
    rows = load_csv(filepath)
    count = 0
    for row in rows:
        existing = db.query(Ouvrage).filter(Ouvrage.code == row["code"]).first()
        if existing:
            continue
        ouvrage = Ouvrage(
            code=row["code"],
            nom=row["nom"],
            famille=row["famille"],
            lat=float(row["lat"]),
            lon=float(row["lon"]),
            classe=row["classe"],
            icf=float(row["icf"]) if row.get("icf") else None,
            ivp=float(row["ivp"]) if row.get("ivp") else None,
            ipd=float(row["ipd"]) if row.get("ipd") else None,
            ied=float(row["ied"]) if row.get("ied") else None,
            exposition=row.get("exposition"),
        )
        db.add(ouvrage)
        count += 1
    db.commit()
    print(f"  [OK] {count} ouvrages insérés")


def seed_pathologies(db):
    """Seed the pathologies reference table."""
    filepath = settings.SEED_DIR / "pathologies.csv"
    rows = load_csv(filepath)
    count = 0
    for row in rows:
        existing = db.query(Pathologie).filter(Pathologie.code == row["code"]).first()
        if existing:
            continue
        patho = Pathologie(
            code=row["code"],
            famille=row.get("famille"),
            description=row.get("description"),
            symptomes=row.get("symptomes"),
            methodes=row.get("methodes"),
            mecanismes=row.get("mecanismes"),
        )
        db.add(patho)
        count += 1
    db.commit()
    print(f"  [OK] {count} pathologies insérées")


def seed_proba(db):
    """Seed the probability matrix from p0_initial.csv."""
    filepath = settings.SEED_DIR / "p0_initial.csv"
    rows = load_csv(filepath)
    count = 0
    pathology_codes = [f"P{i}" for i in range(1, 13)]

    for row in rows:
        ouvrage = db.query(Ouvrage).filter(Ouvrage.code == row["ouvrage_code"]).first()
        if not ouvrage:
            print(f"  [!] Ouvrage {row['ouvrage_code']} non trouvé — ignoré")
            continue

        for code in pathology_codes:
            value = row.get(code)
            if value is None:
                continue
            p0_val = float(value)
            existing = (
                db.query(Proba)
                .filter(Proba.ouvrage_id == ouvrage.id, Proba.pathologie == code)
                .first()
            )
            if existing:
                continue
            proba = Proba(
                ouvrage_id=ouvrage.id,
                pathologie=code,
                p0=p0_val,
                p_current=p0_val,  # initial: p_current = p0
                source="seed_p0_initial",
                computed_by="système — données initiales",
            )
            db.add(proba)
            count += 1
    db.commit()
    print(f"  [OK] {count} probabilités P0 insérées")


def seed_actions(db):
    """Seed the maintenance actions catalog."""
    filepath = settings.SEED_DIR / "actions_maintenance.csv"
    rows = load_csv(filepath)
    count = 0
    for row in rows:
        ouvrage = db.query(Ouvrage).filter(Ouvrage.code == row["ouvrage_code"]).first()
        if not ouvrage:
            print(f"  [!] Ouvrage {row['ouvrage_code']} non trouvé — ignoré")
            continue
        existing = db.query(Action).filter(Action.id == int(row["id"])).first()
        if existing:
            continue
        action = Action(
            id=int(row["id"]),
            ouvrage_id=ouvrage.id,
            pathologie=row.get("pathologie"),
            type_action=row.get("type_action"),
            cout=float(row["cout_dh"]) if row.get("cout_dh") else None,
            duree_jours=int(row["duree_jours"]) if row.get("duree_jours") else None,
            urgence=row.get("urgence"),
            declencheur=row.get("declencheur"),
            preuve_min=row.get("preuve_min"),
        )
        db.add(action)
        count += 1
    db.commit()
    print(f"  [OK] {count} actions de maintenance insérées")


def main():
    print("=" * 60)
    print("GEODIA SentinelCare GC -- Initialisation de la base de donnees")
    print("=" * 60)

    # Create all tables
    print("\n[+] Creation des tables...")
    Base.metadata.create_all(bind=engine)
    print("  [OK] Tables creees")

    # Seed data
    db = SessionLocal()
    try:
        print("\n[+] Import des ouvrages...")
        seed_ouvrages(db)

        print("\n[+] Import des pathologies P1-P12...")
        seed_pathologies(db)

        print("\n[+] Import de la matrice de probabilites P0...")
        seed_proba(db)

        print("\n[+] Import des actions de maintenance...")
        seed_actions(db)

        print("\n" + "=" * 60)
        print("[OK] Base de donnees initialisee avec succes!")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
