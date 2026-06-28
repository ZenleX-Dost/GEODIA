"""
Ouvrage (structure/asset) ORM model.
Represents one of the 19 reinforced concrete structures at Jorf Lasfar.
"""
from datetime import datetime
from sqlalchemy import (
    Integer, String, Float, DateTime, CheckConstraint, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Ouvrage(Base):
    __tablename__ = "ouvrages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    famille: Mapped[str] = mapped_column(String(50), nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    classe: Mapped[str] = mapped_column(
        String(1),
        CheckConstraint("classe IN ('A','B','C','D')"),
        nullable=False,
    )
    icf: Mapped[float | None] = mapped_column(Float, nullable=True)
    ivp: Mapped[float | None] = mapped_column(Float, nullable=True)
    ipd: Mapped[float | None] = mapped_column(Float, nullable=True)
    ied: Mapped[float | None] = mapped_column(Float, nullable=True)
    exposition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    inspections = relationship("Inspection", back_populates="ouvrage", lazy="dynamic")
    env_timeseries = relationship("EnvTimeseries", back_populates="ouvrage", lazy="dynamic")
    insar_points = relationship("InsarPoint", back_populates="ouvrage", lazy="dynamic")
    probas = relationship("Proba", back_populates="ouvrage", lazy="dynamic")
    actions = relationship("Action", back_populates="ouvrage", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Ouvrage {self.code} — {self.nom} (classe {self.classe})>"
