"""
GEODIA — Test Configuration & Shared Fixtures
Uses an in-memory SQLite DB so tests are isolated, fast, and portable.
"""
import pytest
from datetime import date, datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# ─── In-memory test database ───────────────────────────────────────────────────
TEST_DB_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once per test session."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional test DB session that rolls back after each test."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with DB dependency override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


# ─── Seed helpers ──────────────────────────────────────────────────────────────

@pytest.fixture
def seed_ouvrage(db_session):
    """Insert a minimal Ouvrage row and return it."""
    from app.models.ouvrage import Ouvrage

    ouvrage = Ouvrage(
        code="OUV-TEST-01",
        nom="Structure de Test A",
        famille="Dalle",
        lat=33.1,
        lon=-8.6,
        classe="A",
        icf=72.0,
        ivp=65.0,
        ipd=68.0,
        ied=0.55,
        exposition="Marine",
    )
    db_session.add(ouvrage)
    db_session.commit()
    db_session.refresh(ouvrage)
    return ouvrage


@pytest.fixture
def seed_inspection(db_session, seed_ouvrage):
    """Insert a minimal Inspection linked to seed_ouvrage."""
    from app.models.inspection import Inspection

    insp = Inspection(
        ouvrage_id=seed_ouvrage.id,
        date=date(2025, 3, 15),
        inspecteur="Ahmed Benzekri",
        etat="E1",
        commentaire="Inspection initiale",
        validation=False,
    )
    db_session.add(insp)
    db_session.commit()
    db_session.refresh(insp)
    return insp


@pytest.fixture
def seed_insar(db_session, seed_ouvrage):
    """Insert 3 InSAR points (one anomaly, two normal) for seed_ouvrage."""
    from app.models.insar_point import InsarPoint

    pts = [
        InsarPoint(
            ouvrage_id=seed_ouvrage.id,
            lat=33.101, lon=-8.601,
            vitesse_los=-7.5, cumul=-22.0,
            iad=0.85, source="Sentinel-1",
            is_simulated=True,
        ),
        InsarPoint(
            ouvrage_id=seed_ouvrage.id,
            lat=33.102, lon=-8.602,
            vitesse_los=-2.0, cumul=-5.0,
            iad=0.30, source="Sentinel-1",
            is_simulated=True,
        ),
        InsarPoint(
            ouvrage_id=seed_ouvrage.id,
            lat=33.103, lon=-8.603,
            vitesse_los=-1.0, cumul=-3.0,
            iad=0.10, source="Sentinel-1",
            is_simulated=True,
        ),
    ]
    for p in pts:
        db_session.add(p)
    db_session.commit()
    return pts


@pytest.fixture
def seed_action(db_session, seed_ouvrage):
    """Insert a maintenance action for seed_ouvrage."""
    from app.models.action import Action

    action = Action(
        ouvrage_id=seed_ouvrage.id,
        pathologie="P2",
        type_action="Traitement anticorrosion",
        cout=120_000.0,
        duree_jours=14,
        urgence="0-3m",
        statut="planifié",
    )
    db_session.add(action)
    db_session.commit()
    db_session.refresh(action)
    return action


@pytest.fixture
def seed_pathologie(db_session):
    """Insert P2 and P8 pathologie reference rows (needed for Proba FK)."""
    from app.models.pathologie import Pathologie

    codes = ["P2", "P8", "P9", "P12"]
    for code in codes:
        existing = db_session.query(Pathologie).filter(Pathologie.code == code).first()
        if not existing:
            p = Pathologie(code=code, famille="Test", description=f"Pathologie {code}")
            db_session.add(p)
    db_session.commit()


@pytest.fixture
def seed_proba(db_session, seed_ouvrage, seed_pathologie):
    """Insert Proba rows for seed_ouvrage."""
    from app.models.proba import Proba

    probas = [
        Proba(ouvrage_id=seed_ouvrage.id, pathologie="P2",
              p0=25.0, p_current=65.0, iae=0.7, iad=0.85),
        Proba(ouvrage_id=seed_ouvrage.id, pathologie="P8",
              p0=10.0, p_current=40.0, iae=0.7, iad=0.85),
    ]
    for p in probas:
        db_session.add(p)
    db_session.commit()
    return probas


@pytest.fixture
def seed_env(db_session, seed_ouvrage):
    """Insert EnvTimeseries row for seed_ouvrage."""
    from app.models.env_timeseries import EnvTimeseries

    rec = EnvTimeseries(
        ouvrage_id=seed_ouvrage.id,
        date=datetime.utcnow(),
        temperature=22.5,
        humidite=78.0,
        pluie=0.0,
        vent=15.0,
        pollution_so2=12.0,
        pollution_no2=18.0,
        ndwi=0.4,
        iae=0.68,
        source="NASA Test",
        fraicheur="test",
        is_simulated=True,
    )
    db_session.add(rec)
    db_session.commit()
    return rec
