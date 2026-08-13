"""
Main Analysis Service - orchestrates all engines.
"""
from typing import Dict, List, Any, Optional
import json
from pathlib import Path

from ..graph.engine import GraphEngine
from ..gravity.engine import GravityEngine, GravityWeights
from ..gravity.propagation import GravityPropagator, PropagationConfig
from ..gravity.metrics import GravityMetrics
from ..graph.path_analyzer import PathAnalyzer
from ..graph.criticality import CriticalityAnalyzer
from ..graph.blast_radius import BlastRadiusAnalyzer

class AnalysisService:
    """Central service for CERBERUS GRAVITY analysis."""
    
    def __init__(self):
        self.graph_engine = GraphEngine()
        self.gravity_engine = GravityEngine()
        self.propagator = GravityPropagator()
        self.dataset_name = "empty"
        self._last_results: Dict[str, Any] = {}
    
    def load_dataset(self, path: str) -> Dict[str, Any]:
        """Load a JSON dataset."""
        with open(path, "r") as f:
            data = json.load(f)
        self.graph_engine.load_from_dict(data)
        self.dataset_name = data.get("name", Path(path).stem)
        
        # Compute initial gravity
        assets = []
        for n, d in self.graph_engine.graph.nodes(data=True):
            if d.get("node_type") == "asset":
                assets.append({"id": n, **d})
        self.gravity_engine.compute_batch(assets)
        for a in assets:
            self.graph_engine.update_node_attr(a["id"], gravity=a["gravity"])
        
        return {
            "name": self.dataset_name,
            "nodes": self.graph_engine.graph.number_of_nodes(),
            "edges": self.graph_engine.graph.number_of_edges(),
            "message": "Dataset loaded and gravity computed",
        }
    
    def get_gravity_map(self) -> Dict[str, float]:
        return {
            n: d.get("gravity", 0.0)
            for n, d in self.graph_engine.graph.nodes(data=True)
        }
    
    def run_full_analysis(
        self,
        entry_points: Optional[List[str]] = None,
        objective: Optional[str] = None,
        path_mode: str = "strategic",
    ) -> Dict[str, Any]:
        """Run complete analysis pipeline."""
        gmap = self.get_gravity_map()
        
        # Propagation
        influenced = self.propagator.propagate(self.graph_engine.graph, gmap)
        gradients = self.propagator.compute_gravity_gradient(self.graph_engine.graph, gmap)
        
        # Criticality
        crit = CriticalityAnalyzer(self.graph_engine.graph, gmap)
        centralities = crit.compute_centralities()
        strategic = crit.strategic_criticality(centralities)
        wells = crit.detect_gravity_wells()
        
        # Metrics
        concentration = GravityMetrics.gravity_concentration(gmap)
        well_density = GravityMetrics.gravity_well_density(gmap)
        entropy = GravityMetrics.attack_surface_entropy(gmap)
        
        # Paths
        paths = []
        if entry_points and objective:
            analyzer = PathAnalyzer(self.graph_engine.graph, gmap)
            paths = analyzer.find_all_to_objective(entry_points, objective, mode=path_mode)
        
        # Distribution
        dist = {"LOW": 0, "MODERATE": 0, "HIGH": 0, "VERY_HIGH": 0, "CRITICAL": 0}
        for g in gmap.values():
            if g <= 20:
                dist["LOW"] += 1
            elif g <= 40:
                dist["MODERATE"] += 1
            elif g <= 60:
                dist["HIGH"] += 1
            elif g <= 80:
                dist["VERY_HIGH"] += 1
            else:
                dist["CRITICAL"] += 1
        
        top_assets = sorted(
            [{"id": n, "name": self.graph_engine.graph.nodes[n].get("name", n), "gravity": g}
             for n, g in gmap.items()],
            key=lambda x: -x["gravity"],
        )[:10]
        
        result = {
            "dataset": self.dataset_name,
            "gravity_map": gmap,
            "influenced_gravity": influenced,
            "gravity_gradients": gradients,
            "centralities": centralities,
            "strategic_criticality": strategic,
            "gravity_wells": wells,
            "metrics": {
                "gravity_concentration": concentration,
                "gravity_well_density": well_density,
                "attack_surface_entropy": entropy,
                "node_count": self.graph_engine.graph.number_of_nodes(),
                "edge_count": self.graph_engine.graph.number_of_edges(),
            },
            "gravity_distribution": dist,
            "top_gravity_assets": top_assets,
            "attack_paths": paths[:15],
            "graph": self.graph_engine.to_dict(),
            "disclaimer": (
                "All metrics are experimental research constructs of CERBERUS GRAVITY. "
                "They are not industry-standard risk scores and must not be treated as such."
            ),
        }
        self._last_results = result
        return result
    
    def blast_radius(self, node_id: str) -> Dict[str, Any]:
        gmap = self.get_gravity_map()
        analyzer = BlastRadiusAnalyzer(self.graph_engine.graph, gmap)
        return analyzer.compute(node_id)
    
    def simulate_remediation(self, node_id: str, action: str) -> Dict[str, Any]:
        gmap = self.get_gravity_map()
        analyzer = BlastRadiusAnalyzer(self.graph_engine.graph, gmap)
        return analyzer.remediation_impact(
            node_id, action, self.graph_engine, self.gravity_engine
        )
    
    def update_weights(self, weights: Dict[str, float]) -> Dict[str, Any]:
        self.gravity_engine.update_weights(weights)
        # Recompute
        assets = []
        for n, d in self.graph_engine.graph.nodes(data=True):
            if d.get("node_type") == "asset":
                assets.append({"id": n, **d})
        self.gravity_engine.compute_batch(assets)
        for a in assets:
            self.graph_engine.update_node_attr(a["id"], gravity=a["gravity"])
        return {"message": "Weights updated and gravity recomputed", "weights": self.gravity_engine.weights.to_dict()}
    
    def what_if(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Apply a list of changes and return before/after summary.
        Each change: {"node_id": ..., "action": ..., "value": optional}
        """
        before = self.run_full_analysis()
        # Apply on clone conceptually - for simplicity apply then we can reload
        # In production we'd keep a transaction; here we mutate and report.
        for ch in changes:
            nid = ch.get("node_id")
            action = ch.get("action")
            if action == "set_privilege":
                self.graph_engine.update_node_attr(nid, privilege_level=float(ch.get("value", 20)))
            elif action == "set_exposure":
                self.graph_engine.update_node_attr(nid, exposure=float(ch.get("value", 20)))
            elif action == "set_criticality":
                self.graph_engine.update_node_attr(nid, criticality=float(ch.get("value", 20)))
            elif action == "remove_edge":
                self.graph_engine.remove_edge(ch.get("source"), ch.get("target"))
        
        # Recompute gravity
        assets = []
        for n, d in self.graph_engine.graph.nodes(data=True):
            if d.get("node_type") == "asset":
                assets.append({"id": n, **d})
        self.gravity_engine.compute_batch(assets)
        for a in assets:
            self.graph_engine.update_node_attr(a["id"], gravity=a["gravity"])
        
        after = self.run_full_analysis()
        
        return {
            "before_summary": {
                "top_gravity": before["top_gravity_assets"][:5],
                "wells": before["gravity_wells"]["total_wells"],
                "concentration": before["metrics"]["gravity_concentration"],
            },
            "after_summary": {
                "top_gravity": after["top_gravity_assets"][:5],
                "wells": after["gravity_wells"]["total_wells"],
                "concentration": after["metrics"]["gravity_concentration"],
            },
            "note": "Modelled what-if results. Graph state has been updated.",
        }
