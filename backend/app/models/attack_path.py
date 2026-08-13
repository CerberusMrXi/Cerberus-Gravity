"""Attack Path model."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, JSON, Text
from .base import Base, generate_uuid
from typing import Optional, List, Dict, Any

class AttackPath(Base):
    __tablename__ = "attack_paths"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    nodes: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    edges: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    distance: Mapped[float] = mapped_column(Float, default=0.0)
    gravity: Mapped[float] = mapped_column(Float, default=0.0)
    risk: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.7)
    objective: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        return f"<AttackPath(id={self.id}, gravity={self.gravity:.1f}, risk={self.risk:.1f})>"
