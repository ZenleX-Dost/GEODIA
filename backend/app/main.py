"""
GÉODIA SentinelCare GC — FastAPI Application Entrypoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.routers import assets, alerts, inspections, reports, compute, imports, insar, maintenance, env, area

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables on startup (development only)."""
    Base.metadata.create_all(bind=engine)
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Plateforme d'aide à la décision pour la maintenance préventive "
        "de 19 ouvrages en béton armé — OCP Jorf Lasfar"
    ),
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(assets.router)
app.include_router(alerts.router)
app.include_router(inspections.router)
app.include_router(reports.router)
app.include_router(compute.router)
app.include_router(imports.router)
app.include_router(env.router)
app.include_router(insar.router)
app.include_router(maintenance.router)
app.include_router(area.router)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
