"""Research Experiment model."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON, Float, func
from .base import Base, generate_uuid
from typing import Optional, Dict, Any
from datetime import datetime

class Experiment(Base):
    __tablename__ = "experiments"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    configuration: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    dataset: Mapped[str] = mapped_column(String(255), default="demo")
    results: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Experiment(name={self.name})>"
