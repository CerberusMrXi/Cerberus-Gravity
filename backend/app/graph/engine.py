"""
Graph Construction & Management Engine
======================================
Builds and maintains the NetworkX attack graph from assets and relationships.
"""
from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
from copy import deepcopy

class GraphEngine:
    """Core graph construction and query engine."""
    
    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.assets: Dict[str, Dict[str, Any]] = {}
        self.identities: Dict[str, Dict[str, Any]] = {}
    
    def clear(self) -> None:
        self.graph.clear()
        self.assets.clear()
        self.identities.clear()
    
    def add_asset(self, asset: Dict[str, Any]) -> None:
        """Add or update an asset node."""
        node_id = asset["id"]
        self.assets[node_id] = asset
        self.graph.add_node(
            node_id,
            **{k: v for k, v in asset.items() if k != "id"},
            node_type="asset",
        )
    
    def add_identity(self, identity: Dict[str, Any]) -> None:
        """Add an identity node."""
        node_id = identity["id"]
        self.identities[node_id] = identity
        self.graph.add_node(
            node_id,
            **{k: v for k, v in identity.items() if k != "id"},
            node_type="identity",
        )
    
    def add_relationship(self, rel: Dict[str, Any]) -> None:
        """Add a directed relationship edge."""
        src = rel["source"]
        tgt = rel["target"]
        if src not in self.graph or tgt not in self.graph:
            return  # skip dangling
        self.graph.add_edge(
            src,
            tgt,
            relationship_type=rel.get("relationship_type", "access"),
            trust=rel.get("trust", 50.0),
            permission=rel.get("permission", "read"),
            distance=rel.get("distance", 1.0),
            confidence=rel.get("confidence", 0.8),
        )
    
    def load_from_dict(self, data: Dict[str, Any]) -> None:
        """Load full graph from a dataset dict."""
        self.clear()
        for asset in data.get("assets", []):
            self.add_asset(asset)
        for identity in data.get("identities", []):
            self.add_identity(identity)
        for rel in data.get("relationships", []):
            self.add_relationship(rel)
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        if node_id in self.graph:
            return {"id": node_id, **self.graph.nodes[node_id]}
        return None
    
    def get_neighbors(self, node_id: str, direction: str = "out") -> List[str]:
        if node_id not in self.graph:
            return []
        if direction == "out":
            return list(self.graph.successors(node_id))
        elif direction == "in":
            return list(self.graph.predecessors(node_id))
        else:
            return list(set(self.graph.successors(node_id)) | set(self.graph.predecessors(node_id)))
    
    def to_dict(self) -> Dict[str, Any]:
        """Export graph as serializable dict."""
        nodes = []
        for n, data in self.graph.nodes(data=True):
            nodes.append({"id": n, **data})
        edges = []
        for u, v, data in self.graph.edges(data=True):
            edges.append({"source": u, "target": v, **data})
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges(),
            },
        }
    
    def update_node_attr(self, node_id: str, **attrs) -> bool:
        if node_id not in self.graph:
            return False
        for k, v in attrs.items():
            self.graph.nodes[node_id][k] = v
            if node_id in self.assets:
                self.assets[node_id][k] = v
        return True
    
    def remove_edge(self, source: str, target: str) -> bool:
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
            return True
        return False
    
    def clone(self) -> "GraphEngine":
        """Deep copy for what-if simulations."""
        new = GraphEngine()
        new.graph = self.graph.copy()
        new.assets = deepcopy(self.assets)
        new.identities = deepcopy(self.identities)
        return new
