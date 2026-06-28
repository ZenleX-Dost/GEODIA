"""
Pathologie reference model (P1–P12).
Defines the 12 concrete pathology types relevant to marine/chemical environments.
"""
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Pathologie(Base):
    __tablename__ = "pathologies"

    code: Mapped[str] = mapped_column(String(5), primary_key=True)  # P1..P12
    famille: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    symptomes: Mapped[str | None] = mapped_column(Text, nullable=True)
    methodes: Mapped[str | None] = mapped_column(Text, nullable=True)  # CND methods
    mecanismes: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Pathologie {self.code}>"
