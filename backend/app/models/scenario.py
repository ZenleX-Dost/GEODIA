"""
Scenario model — budget optimization scenarios.
"""
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str | None] = mapped_column(String(20), nullable=True)  # S1/S2/S3
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    actions_retenues: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array of action IDs
    risque_initial: Mapped[float | None] = mapped_column(Float, nullable=True)
    risque_final: Mapped[float | None] = mapped_column(Float, nullable=True)
    gain_risque: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Scenario {self.nom} budget={self.budget}>"
