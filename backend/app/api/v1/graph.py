from fastapi import APIRouter
from .analysis import _service as svc

router = APIRouter()

@router.get("/")
async def get_graph():
    return svc.graph_engine.to_dict()

@router.get("/nodes")
async def list_nodes():
    nodes = [{"id": n, **d} for n, d in svc.graph_engine.graph.nodes(data=True)]
    return {"nodes": nodes}
