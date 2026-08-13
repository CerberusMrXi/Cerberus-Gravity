"""
Gravity Propagation Algorithm
=============================
High-gravity nodes influence neighboring nodes based on graph distance,
relationship strength, trust, and privilege transitions.

This is an experimental research model.
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import networkx as nx
import math

@dataclass
class PropagationConfig:
    decay_factor: float = 0.6
    max_propagation_distance: int = 5
    relationship_weight: float = 1.0
    trust_weight: float = 0.9
    privilege_transition_bonus: float = 0.15  # extra influence when privilege increases


class GravityPropagator:
    """
    Propagates gravity influence through the attack graph.
    
    Influence from source to target decreases with distance:
        influence = source_gravity * (decay_factor ** distance) * relationship_factor * trust_factor
    """
    
    def __init__(self, config: Optional[PropagationConfig] = None):
        self.config = config or PropagationConfig()
    
    def propagate(
        self,
        graph: nx.DiGraph,
        gravity_map: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Compute propagated gravity influence for every node.
        
        Returns a dict of node_id -> total_influenced_gravity
        (base gravity + received influence from higher gravity nodes).
        """
        influenced = {n: gravity_map.get(n, 0.0) for n in graph.nodes()}
        cfg = self.config
        
        # For each high-gravity node, push influence outward
        for source in graph.nodes():
            src_g = gravity_map.get(source, 0.0)
            if src_g < 10.0:  # skip low gravity
                continue
            
            # BFS / shortest path distances
            try:
                lengths = nx.single_source_shortest_path_length(
                    graph, source, cutoff=cfg.max_propagation_distance
                )
            except nx.NetworkXError:
                continue
            
            for target, dist in lengths.items():
                if dist == 0:
                    continue
                
                # Relationship factor
                edge_data = graph.get_edge_data(source, target) or {}
                # For multi-hop, approximate using path
                rel_strength = edge_data.get("trust", 50.0) / 100.0 if dist == 1 else 0.7
                trust_f = (rel_strength ** cfg.trust_weight) * cfg.relationship_weight
                
                # Decay
                decay = cfg.decay_factor ** dist
                
                influence = src_g * decay * trust_f
                
                # Privilege transition bonus (if moving toward higher privilege)
                tgt_priv = graph.nodes[target].get("privilege_level", 30.0)
                src_priv = graph.nodes[source].get("privilege_level", 30.0)
                if tgt_priv > src_priv:
                    influence *= (1.0 + cfg.privilege_transition_bonus)
                
                influenced[target] = influenced.get(target, 0.0) + influence * 0.3  # dampen
        
        # Cap at 100
        for n in influenced:
            influenced[n] = min(100.0, round(influenced[n], 2))
        
        return influenced
    
    def compute_gravity_gradient(
        self,
        graph: nx.DiGraph,
        gravity_map: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Gravity Gradient: how steeply gravity changes around a node.
        Higher gradient indicates potential "pull" toward gravity wells.
        """
        gradients = {}
        for node in graph.nodes():
            neighbors = list(graph.successors(node)) + list(graph.predecessors(node))
            if not neighbors:
                gradients[node] = 0.0
                continue
            node_g = gravity_map.get(node, 0.0)
            diffs = [abs(gravity_map.get(nb, 0.0) - node_g) for nb in neighbors]
            gradients[node] = round(sum(diffs) / len(diffs), 2)
        return gradients
