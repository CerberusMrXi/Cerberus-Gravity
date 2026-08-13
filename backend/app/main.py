"""
CERBERUS GRAVITY
Risk-Weighted Attack Graph Intelligence Engine

Author: Sudeepa Wanigarathna
© 2026 Sudeepa Wanigarathna
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

from .core.config import settings
from .api.v1 import api_router
from .services.analysis import AnalysisService

analysis_service = AnalysisService()


def _find_datasets_dir() -> Path:
    """Resolve datasets directory from multiple possible locations."""
    candidates = [
        Path(__file__).resolve().parents[2] / "datasets",  # repo root when running from backend/app
        Path(__file__).resolve().parents[3] / "datasets",
        Path.cwd().parent / "datasets",
        Path.cwd() / "datasets",
        Path.cwd() / ".." / "datasets",
    ]
    for c in candidates:
        c = c.resolve()
        if c.is_dir() and any(c.glob("*.json")):
            return c
    return candidates[0]


@asynccontextmanager
async def lifespan(app: FastAPI):
    datasets = _find_datasets_dir()
    demo = datasets / "demo_lab.json"
    if demo.exists():
        analysis_service.load_dataset(str(demo))
        print(f"[CERBERUS] Dataset loaded: {demo}")
    else:
        print(f"[CERBERUS] No demo dataset at {demo} — load via API")
    # share service with routers
    from .api.v1 import analysis as analysis_module
    analysis_module._service = analysis_service
    analysis_module.DATASETS_DIR = datasets
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION + " | Experimental research model — not an industry standard.",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "project": "CERBERUS GRAVITY",
        "tagline": "Risk-Weighted Attack Graph Intelligence Engine",
        "author": "Sudeepa Wanigarathna",
        "version": settings.VERSION,
        "docs": "/docs",
        "disclaimer": (
            "This is an experimental cybersecurity research platform. "
            "All gravity and risk metrics are research constructs, "
            "not established industry standards."
        ),
    }
