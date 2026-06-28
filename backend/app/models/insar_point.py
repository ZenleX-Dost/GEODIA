"""
InsarPoint model — InSAR deformation measurement points per structure.
"""
from datetime import date
from sqlalchemy import (
    Integer, String, Float, Date, Boolean, Text, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InsarPoint(Base):
    __tablename__ = "insar_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ouvrage_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ouvrages.id"), nullable=False
    )
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    date_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    vitesse_los: Mapped[float | None] = mapped_column(Float, nullable=True)  # mm/year
    cumul: Mapped[float | None] = mapped_column(Float, nullable=True)  # mm total
    acceleration: Mapped[float | None] = mapped_column(Float, nullable=True)
    r2: Mapped[float | None] = mapped_column(Float, nullable=True)
    cluster_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    iad: Mapped[float | None] = mapped_column(Float, nullable=True)  # computed IAD
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    ouvrage = relationship("Ouvrage", back_populates="insar_points")

    def __repr__(self) -> str:
        return f"<InsarPoint {self.id} — ouvrage={self.ouvrage_id} v_los={self.vitesse_los}>"
