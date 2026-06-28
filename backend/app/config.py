"""
Configuration settings for the GÉODIA backend.
Uses pydantic-settings for environment variable support.
"""
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""

    # --- Application ---
    APP_NAME: str = "GEODIA SentinelCare GC"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # --- Database (SQLite for V1 prototype) ---
    # To switch to PostgreSQL later, change this to:
    # DB_URL: str = "postgresql://user:pass@localhost:5432/geodia"
    DB_URL: str = ""

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        # Default: SQLite in the backend directory
        db_path = self.BASE_DIR / "geodia.db"
        return f"sqlite:///{db_path}"

    # --- CORS ---
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # --- Paths ---
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    SEED_DIR: Path = BASE_DIR / "data" / "seed"
    SIMULATED_DIR: Path = BASE_DIR / "data" / "simulated"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
