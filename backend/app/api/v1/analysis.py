from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime, timezone

from ...services.analysis import AnalysisService
from ...schemas.analysis import (
    GravityWeightsSchema,
    RemediationRequest,
    WhatIfRequest,
)

router = APIRouter()
_service = AnalysisService()
DATASETS_DIR = Path(__file__).resolve().parents[4] / "datasets"
EXPERIMENTS_DIR = Path(__file__).resolve().parents[4] / "experiments"


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "project": "CERBERUS GRAVITY",
        "author": "Sudeepa Wanigarathna",
        "version": "1.0.0",
        "nodes": _service.graph_engine.graph.number_of_nodes(),
    }


@router.post("/load/{dataset_name}")
async def load_dataset(dataset_name: str):
    path = DATASETS_DIR / f"{dataset_name}.json"
    if not path.exists():
        raise HTTPException(404, f"Dataset '{dataset_name}' not found in {DATASETS_DIR}")
    return _service.load_dataset(str(path))


@router.get("/full")
async def full_analysis(
    entry: Optional[str] = Query(None, description="Comma-separated entry points"),
    objective: Optional[str] = Query(None),
    mode: str = Query("strategic"),
):
    g = _service.graph_engine.graph
    if g.number_of_nodes() == 0:
        raise HTTPException(400, "No graph loaded. POST /api/v1/analysis/load/{dataset_name} first.")
    # auto-pick sensible defaults from graph
    entries = entry.split(",") if entry else None
    if not entries:
        # prefer internet/edge style nodes
        for n, d in g.nodes(data=True):
            if "inet" in n.lower() or d.get("type") == "network":
                entries = [n]
                break
        if not entries:
            entries = [list(g.nodes())[0]]
    obj = objective
    if not obj:
        for n, d in g.nodes(data=True):
            if "crit" in n.lower() or (d.get("criticality") or 0) >= 90:
                obj = n
                break
        if not obj:
            obj = list(g.nodes())[-1]
    return _service.run_full_analysis(entry_points=entries, objective=obj, path_mode=mode)


@router.get("/gravity")
async def get_gravity():
    return {"gravity_map": _service.get_gravity_map()}


@router.post("/weights")
async def update_weights(weights: GravityWeightsSchema):
    return _service.update_weights(weights.model_dump())


@router.get("/blast/{node_id}")
async def blast_radius(node_id: str):
    result = _service.blast_radius(node_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result


@router.post("/remediate")
async def remediate(req: RemediationRequest):
    return _service.simulate_remediation(req.node_id, req.action)


@router.post("/what-if")
async def what_if(req: WhatIfRequest):
    changes = [c.model_dump() for c in req.changes]
    return _service.what_if(changes)


@router.get("/datasets")
async def list_datasets():
    if not DATASETS_DIR.exists():
        return {"datasets": [], "path": str(DATASETS_DIR)}
    files = list(DATASETS_DIR.glob("*.json"))
    return {"datasets": [f.stem for f in files], "path": str(DATASETS_DIR)}


@router.post("/experiments")
async def save_experiment(payload: Dict[str, Any] = Body(...)):
    """Save a research experiment configuration + results snapshot."""
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    exp_id = payload.get("id") or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = payload.get("name") or f"experiment_{exp_id}"
    record = {
        "id": exp_id,
        "name": name,
        "description": payload.get("description", ""),
        "configuration": payload.get("configuration", {}),
        "dataset": payload.get("dataset", _service.dataset_name),
        "results": payload.get("results"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    path = EXPERIMENTS_DIR / f"{exp_id}.json"
    path.write_text(json.dumps(record, indent=2))
    return {"saved": True, "id": exp_id, "path": str(path)}


@router.get("/experiments")
async def list_experiments():
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for f in sorted(EXPERIMENTS_DIR.glob("*.json"), reverse=True):
        try:
            items.append(json.loads(f.read_text()))
        except Exception:
            continue
    return {"experiments": items}


@router.get("/experiments/{exp_id}")
async def get_experiment(exp_id: str):
    path = EXPERIMENTS_DIR / f"{exp_id}.json"
    if not path.exists():
        raise HTTPException(404, "Experiment not found")
    return json.loads(path.read_text())
