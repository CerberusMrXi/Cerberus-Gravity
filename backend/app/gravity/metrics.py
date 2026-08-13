"""
Experimental Gravity Metrics
============================
All metrics are research constructs, not established security standards.
"""
from typing import Dict, List, Any, Optional
import networkx as nx
import math
from collections import Counter

class GravityMetrics:
    """Collection of experimental gravity-related metrics."""
    
    @staticmethod
    def gravity_concentration(gravity_map: Dict[str, float]) -> float:
        """
        Gravity Concentration (Gini-like).
        0 = perfectly equal, 1 = all gravity in one node.
        """
        values = sorted(gravity_map.values())
        n = len(values)
        if n == 0:
            return 0.0
        total = sum(values)
        if total == 0:
            return 0.0
        cum = 0.0
        gini = 0.0
        for i, v in enumerate(values):
            cum += v
            gini += (2 * (i + 1) - n - 1) * v
        return round(abs(gini) / (n * total), 4)
    
    @staticmethod
    def gravity_well_density(
        gravity_map: Dict[str, float],
        threshold: float = 70.0,
    ) -> Dict[str, Any]:
        """Count and characterize gravity wells (nodes above threshold)."""
        wells = {k: v for k, v in gravity_map.items() if v >= threshold}
        return {
            "count": len(wells),
            "density": round(len(wells) / max(1, len(gravity_map)), 4),
            "wells": wells,
            "threshold": threshold,
        }
    
    @staticmethod
    def attack_surface_entropy(gravity_map: Dict[str, float], bins: int = 5) -> float:
        """
        Attack Surface Entropy: Shannon entropy of gravity distribution.
        Higher = more uniform risk surface; lower = concentrated.
        """
        if not gravity_map:
            return 0.0
        values = list(gravity_map.values())
        # Bin into bins
        hist = [0] * bins
        for v in values:
            idx = min(bins - 1, int(v / (100.0 / bins)))
            hist[idx] += 1
        total = sum(hist)
        if total == 0:
            return 0.0
        entropy = 0.0
        for h in hist:
            if h > 0:
                p = h / total
                entropy -= p * math.log2(p)
        return round(entropy, 4)
    
    @staticmethod
    def strategic_attraction(
        path_gravity: float,
        path_distance: float,
        max_node_gravity: float,
        risk: float,
    ) -> float:
        """
        Strategic Attraction score for a path.
        Balances gravity, short distance, high max gravity, moderate risk.
        Experimental formula.
        """
        if path_distance <= 0:
            path_distance = 1.0
        # Prefer high gravity, low distance, high peak, controlled risk
        score = (
            0.35 * path_gravity +
            0.25 * max_node_gravity +
            0.20 * (100.0 / path_distance) +  # inverse distance
            0.20 * risk
        )
        return round(min(100.0, score), 2)
    
    @staticmethod
    def path_efficiency(path_gravity: float, path_distance: float) -> float:
        """Gravity gained per hop."""
        if path_distance <= 0:
            return path_gravity
        return round(path_gravity / path_distance, 2)
