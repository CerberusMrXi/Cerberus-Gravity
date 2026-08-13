"""Relationship (edge) model."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Text
from .base import Base, generate_uuid
from typing import Optional

class Relationship(Base):
    __tablename__ = "relationships"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    source: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    target: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False)  # trust, access, dependency, etc.
    trust: Mapped[float] = mapped_column(Float, default=50.0)
    permission: Mapped[str] = mapped_column(String(100), default="read")
    distance: Mapped[float] = mapped_column(Float, default=1.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.8)
    
    def __repr__(self) -> str:
        return f"<Relationship({self.source} -> {self.target}, type={self.relationship_type})>"
