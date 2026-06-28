"""
Inspection model — field inspection records.
"""
from datetime import datetime, date
from sqlalchemy import (
    Integer, String, Date, DateTime, Boolean, Text, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ouvrage_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ouvrages.id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    inspecteur: Mapped[str] = mapped_column(String(100), nullable=False)
    etat: Mapped[str | None] = mapped_column(
        String(2),
        CheckConstraint("etat IN ('E0','E1','E2','E3')"),
        nullable=True,
    )
    photos: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array of file paths
    commentaire: Mapped[str | None] = mapped_column(Text, nullable=True)
    validation: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    ouvrage = relationship("Ouvrage", back_populates="inspections")
    observations = relationship("Observation", back_populates="inspection", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Inspection {self.id} — ouvrage={self.ouvrage_id} date={self.date}>"
