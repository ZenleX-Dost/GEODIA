"""
Proba model — probability matrix (19 structures × 12 pathologies).
"""
from datetime import datetime
from sqlalchemy import (
    Integer, String, Float, DateTime, Text, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Proba(Base):
    __tablename__ = "proba"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ouvrage_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ouvrages.id"), nullable=False
    )
    pathologie: Mapped[str] = mapped_column(
        String(5), ForeignKey("pathologies.code"), nullable=False
    )
    p0: Mapped[float | None] = mapped_column(Float, nullable=True)  # initial prior %
    p_current: Mapped[float | None] = mapped_column(Float, nullable=True)  # updated probability %
    iae: Mapped[float | None] = mapped_column(Float, nullable=True)
    iad: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    computed_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    ouvrage = relationship("Ouvrage", back_populates="probas")

    def __repr__(self) -> str:
        return f"<Proba ouvrage={self.ouvrage_id} {self.pathologie}={self.p_current}%>"
