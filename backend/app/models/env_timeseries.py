"""
EnvTimeseries model — environmental time series data per structure.
"""
from datetime import datetime
from sqlalchemy import (
    Integer, String, Float, DateTime, Boolean, Text, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EnvTimeseries(Base):
    __tablename__ = "env_timeseries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ouvrage_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ouvrages.id"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidite: Mapped[float | None] = mapped_column(Float, nullable=True)
    pluie: Mapped[float | None] = mapped_column(Float, nullable=True)
    vent: Mapped[float | None] = mapped_column(Float, nullable=True)
    pollution_so2: Mapped[float | None] = mapped_column(Float, nullable=True)
    pollution_no2: Mapped[float | None] = mapped_column(Float, nullable=True)
    ndwi: Mapped[float | None] = mapped_column(Float, nullable=True)  # water index
    iae: Mapped[float | None] = mapped_column(Float, nullable=True)  # computed IAE
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fraicheur: Mapped[str | None] = mapped_column(String(20), nullable=True)  # fresh/stale/simulated
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    ouvrage = relationship("Ouvrage", back_populates="env_timeseries")

    def __repr__(self) -> str:
        return f"<EnvTimeseries ouvrage={self.ouvrage_id} date={self.date}>"
