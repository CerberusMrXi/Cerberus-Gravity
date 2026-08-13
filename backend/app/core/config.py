"""Application configuration for CERBERUS GRAVITY."""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CERBERUS GRAVITY"
    VERSION: str = "0.1.0"
    AUTHOR: str = "Sudeepa Wanigarathna"
    DESCRIPTION: str = "Risk-Weighted Attack Graph Intelligence Engine"
    
    # API
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./cerberus.db"
    
    # Gravity Model Defaults (Experimental Research Model)
    ASSET_VALUE_WEIGHT: float = 1.0
    PRIVILEGE_WEIGHT: float = 1.2
    REACHABILITY_WEIGHT: float = 1.0
    TRUST_WEIGHT: float = 0.8
    EXPOSURE_WEIGHT: float = 1.1
    
    # Propagation Defaults
    DECAY_FACTOR: float = 0.6
    MAX_PROPAGATION_DISTANCE: int = 5
    RELATIONSHIP_WEIGHT: float = 1.0
    PROP_TRUST_WEIGHT: float = 0.9
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production-cerberus-gravity-2026")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
