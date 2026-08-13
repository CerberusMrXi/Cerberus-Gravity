from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GravityWeightsSchema(BaseModel):
    asset_value_weight: float = 1.0
    privilege_weight: float = 1.2
    reachability_weight: float = 1.0
    trust_weight: float = 0.8
    exposure_weight: float = 1.1

class PropagationConfigSchema(BaseModel):
    decay_factor: float = 0.6
    max_propagation_distance: int = 5
    relationship_weight: float = 1.0
    trust_weight: float = 0.9

class PathRequest(BaseModel):
    entry_points: List[str]
    objective: str
    mode: str = "strategic"
    max_paths: int = 10

class RemediationRequest(BaseModel):
    node_id: str
    action: str = Field(..., description="reduce_privilege | reduce_exposure | reduce_criticality | remove_outbound_trust | increase_segmentation")

class WhatIfChange(BaseModel):
    node_id: Optional[str] = None
    action: str
    value: Optional[float] = None
    source: Optional[str] = None
    target: Optional[str] = None

class WhatIfRequest(BaseModel):
    changes: List[WhatIfChange]

class AnalysisResponse(BaseModel):
    dataset: str
    metrics: Dict[str, Any]
    gravity_distribution: Dict[str, int]
    top_gravity_assets: List[Dict[str, Any]]
    gravity_wells: Dict[str, Any]
    disclaimer: str
