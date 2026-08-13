"""Simulation model."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON, Text, func
from .base import Base, generate_uuid
from typing import Optional, List, Dict, Any
from datetime import datetime

class Simulation(Base):
    __tablename__ = "simulations"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    objective: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    paths: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    events: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Simulation(name={self.name})>"
