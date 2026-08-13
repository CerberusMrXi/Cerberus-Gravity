"""
Attack Path Analysis Engine
===========================
Computes multiple ranked paths between initial access and objectives.
"""
from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
from ..gravity.metrics import GravityMetrics

class PathAnalyzer:
    """Analyzes and ranks attack paths."""
    
    def __init__(self, graph: nx.DiGraph, gravity_map: Dict[str, float]):
        self.graph = graph
        self.gravity_map = gravity_map
    
    def find_paths(
        self,
        source: str,
        target: str,
        max_paths: int = 10,
        cutoff: int = 8,
    ) -> List[Dict[str, Any]]:
        """Find simple paths and score them."""
        if source not in self.graph or target not in self.graph:
            return []
        
        try:
            raw_paths = list(nx.all_simple_paths(self.graph, source, target, cutoff=cutoff))
        except (nx.NetworkXError, nx.NodeNotFound):
            return []
        
        # Limit
        raw_paths = raw_paths[: max_paths * 3]  # oversample then rank
        
        scored = []
        for path in raw_paths:
            scored.append(self._score_path(path))
        
        return scored
    
    def _score_path(self, nodes: List[str]) -> Dict[str, Any]:
        """Compute all path metrics."""
        gravity_values = [self.gravity_map.get(n, 0.0) for n in nodes]
        path_gravity = sum(gravity_values)
        avg_gravity = path_gravity / len(nodes) if nodes else 0.0
        max_gravity = max(gravity_values) if gravity_values else 0.0
        distance = len(nodes) - 1
        
        # Privilege transitions
        priv_trans = 0
        for i in range(len(nodes) - 1):
            p1 = self.graph.nodes[nodes[i]].get("privilege_level", 0)
            p2 = self.graph.nodes[nodes[i + 1]].get("privilege_level", 0)
            if p2 > p1:
                priv_trans += 1
        
        # Trust transitions (average edge trust)
        trusts = []
        for i in range(len(nodes) - 1):
            edge = self.graph.get_edge_data(nodes[i], nodes[i + 1]) or {}
            trusts.append(edge.get("trust", 50.0))
        avg_trust = sum(trusts) / len(trusts) if trusts else 50.0
        
        # Risk score (experimental)
        risk = (
            0.4 * avg_gravity +
            0.3 * max_gravity +
            0.2 * (100 - avg_trust) +  # low trust = higher risk? or opposite
            0.1 * (priv_trans * 15)
        )
        risk = min(100.0, risk)
        
        strategic = GravityMetrics.strategic_attraction(
            path_gravity=path_gravity,
            path_distance=float(distance),
            max_node_gravity=max_gravity,
            risk=risk,
        )
        
        efficiency = GravityMetrics.path_efficiency(path_gravity, float(distance))
        
        return {
            "nodes": nodes,
            "distance": distance,
            "path_gravity": round(path_gravity, 2),
            "average_gravity": round(avg_gravity, 2),
            "max_node_gravity": round(max_gravity, 2),
            "privilege_transitions": priv_trans,
            "average_trust": round(avg_trust, 2),
            "risk": round(risk, 2),
            "strategic_attraction": strategic,
            "path_efficiency": efficiency,
            "confidence": 0.75,
        }
    
    def rank_paths(
        self,
        paths: List[Dict[str, Any]],
        mode: str = "strategic",
    ) -> List[Dict[str, Any]]:
        """
        Rank paths by mode:
        - shortest: minimize distance
        - highest_gravity: maximize path_gravity
        - lowest_risk: minimize risk
        - strategic: maximize strategic_attraction
        """
        key_map = {
            "shortest": lambda p: p["distance"],
            "highest_gravity": lambda p: -p["path_gravity"],
            "lowest_risk": lambda p: p["risk"],
            "strategic": lambda p: -p["strategic_attraction"],
        }
        key = key_map.get(mode, key_map["strategic"])
        return sorted(paths, key=key)
    
    def find_all_to_objective(
        self,
        entry_points: List[str],
        objective: str,
        max_per_entry: int = 5,
        mode: str = "strategic",
    ) -> List[Dict[str, Any]]:
        """Find and rank paths from multiple entry points to one objective."""
        all_paths = []
        for entry in entry_points:
            paths = self.find_paths(entry, objective, max_paths=max_per_entry)
            all_paths.extend(paths)
        return self.rank_paths(all_paths, mode=mode)
