"""
Observation model — pathology observations per inspection.
"""
from datetime import datetime
from sqlalchemy import (
    Integer, String, Float, DateTime, Text, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inspections.id"), nullable=False
    )
    pathologie: Mapped[str | None] = mapped_column(
        String(5), ForeignKey("pathologies.code"), nullable=True
    )
    zone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gravite: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("gravite BETWEEN 0 AND 3"),
        nullable=True,
    )
    etendue: Mapped[float | None] = mapped_column(Float, nullable=True)  # % surface affected
    preuve: Mapped[str | None] = mapped_column(Text, nullable=True)  # evidence description
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    inspection = relationship("Inspection", back_populates="observations")

    def __repr__(self) -> str:
        return f"<Observation {self.id} — {self.pathologie} gravité={self.gravite}>"
