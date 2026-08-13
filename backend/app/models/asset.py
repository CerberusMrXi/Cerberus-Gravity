"""Asset model for CERBERUS GRAVITY."""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Integer, JSON, Text
from .base import Base, generate_uuid
from typing import Optional, Dict, Any, List

class Asset(Base):
    __tablename__ = "assets"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)  # server, workstation, database, etc.
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    hostname: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Risk factors (0-100 scale)
    criticality: Mapped[float] = mapped_column(Float, default=50.0)
    privilege_level: Mapped[float] = mapped_column(Float, default=30.0)
    reachability: Mapped[float] = mapped_column(Float, default=40.0)
    exposure: Mapped[float] = mapped_column(Float, default=30.0)
    trust_level: Mapped[float] = mapped_column(Float, default=50.0)
    business_value: Mapped[float] = mapped_column(Float, default=50.0)
    
    # Computed
    gravity: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    
    def __repr__(self) -> str:
        return f"<Asset(id={self.id}, name={self.name}, gravity={self.gravity:.1f})>"
