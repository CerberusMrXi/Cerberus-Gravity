"""Identity model."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, JSON
from .base import Base, generate_uuid
from typing import Optional, Dict, Any, List

class Identity(Base):
    __tablename__ = "identities"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    username: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(100), default="user")
    privilege: Mapped[float] = mapped_column(Float, default=20.0)
    groups: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list)
    trust_relationships: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    
    def __repr__(self) -> str:
        return f"<Identity(username={self.username}, privilege={self.privilege})>"
