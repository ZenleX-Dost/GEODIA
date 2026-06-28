"""
Action model — maintenance action catalog.
"""
from sqlalchemy import (
    Integer, String, Float, Text, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ouvrage_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ouvrages.id"), nullable=False
    )
    pathologie: Mapped[str | None] = mapped_column(String(5), nullable=True)
    type_action: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cout: Mapped[float | None] = mapped_column(Float, nullable=True)  # DH
    duree_jours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    urgence: Mapped[str | None] = mapped_column(
        String(10),
        CheckConstraint("urgence IN ('0-3m','3-6m','6-12m','>12m')"),
        nullable=True,
    )
    statut: Mapped[str] = mapped_column(String(20), default="planifié")
    declencheur: Mapped[str | None] = mapped_column(Text, nullable=True)
    dependances: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array of action IDs
    preuve_min: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    ouvrage = relationship("Ouvrage", back_populates="actions")

    def __repr__(self) -> str:
        return f"<Action {self.id} — {self.type_action} urgence={self.urgence}>"
