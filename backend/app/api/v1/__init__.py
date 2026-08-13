from fastapi import APIRouter
from .analysis import router as analysis_router
from .graph import router as graph_router

api_router = APIRouter()
api_router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(graph_router, prefix="/graph", tags=["Graph"])
