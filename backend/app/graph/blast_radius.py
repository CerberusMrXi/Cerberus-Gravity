"""
Blast Radius Analysis
=====================
"What happens to the attack graph if this node becomes compromised?"
"""
from typing import Dict, List, Any, Optional, Set
import networkx as nx
from copy import deepcopy

class BlastRadiusAnalyzer:
    """Computes blast radius of a compromised node."""
    
    def __init__(self, graph: nx.DiGraph, gravity_map: Dict[str, float]):
        self.graph = graph
        self.gravity_map = gravity_map
    
    def compute(self, node_id: str) -> Dict[str, Any]:
        """Full blast radius report for a node."""
        if node_id not in self.graph:
            return {"error": "Node not found"}
        
        # Reachable nodes if this node is entry
        reachable = set()
        try:
            reachable = set(nx.descendants(self.graph, node_id))
        except Exception:
            pass
        reachable.add(node_id)
        
        # Privileged identities / high privilege assets exposed
        high_priv = []
        critical_exposed = []
        for n in reachable:
            data = self.graph.nodes[n]
            priv = data.get("privilege_level", 0)
            crit = data.get("criticality", 0)
            grav = self.gravity_map.get(n, 0)
            if priv >= 70:
                high_priv.append({"id": n, "privilege": priv, "name": data.get("name", n)})
            if crit >= 70 or grav >= 70:
                critical_exposed.append({
                    "id": n,
                    "criticality": crit,
                    "gravity": grav,
                    "name": data.get("name", n),
                })
        
        # Paths that include this node
        # Approximate: count of simple paths that go through it (expensive, so sample)
        paths_through = self._estimate_paths_through(node_id)
        
        return {
            "node_id": node_id,
            "node_name": self.graph.nodes[node_id].get("name", node_id),
            "reachable_count": len(reachable),
            "reachable_nodes": list(reachable),
            "high_privilege_exposed": high_priv,
            "critical_assets_exposed": critical_exposed,
            "estimated_paths_through": paths_through,
            "blast_score": self._blast_score(reachable, critical_exposed, high_priv),
        }
    
    def _estimate_paths_through(self, node_id: str, sample: int = 20) -> int:
        """Rough estimate of paths traversing the node."""
        # Use betweenness as proxy scaled
        try:
            bc = nx.betweenness_centrality(self.graph, normalized=False)
            return int(bc.get(node_id, 0))
        except Exception:
            return 0
    
    def _blast_score(
        self,
        reachable: Set[str],
        critical: List[Dict],
        high_priv: List[Dict],
    ) -> float:
        """Experimental blast score 0-100."""
        base = min(50.0, len(reachable) * 2.0)
        crit_bonus = len(critical) * 8.0
        priv_bonus = len(high_priv) * 5.0
        return round(min(100.0, base + crit_bonus + priv_bonus), 2)
    
    def remediation_impact(
        self,
        node_id: str,
        action: str,
        graph_engine,  # GraphEngine instance
        gravity_engine,  # GravityEngine
    ) -> Dict[str, Any]:
        """
        Simulate remediation and return before/after comparison.
        Actions: reduce_privilege, reduce_exposure, remove_trust, increase_segmentation, etc.
        """
        # Snapshot before
        before_gravity = dict(self.gravity_map)
        before_blast = self.compute(node_id)
        
        # Clone and apply
        sim = graph_engine.clone()
        
        if action == "reduce_privilege":
            current = sim.graph.nodes[node_id].get("privilege_level", 50)
            sim.update_node_attr(node_id, privilege_level=max(10.0, current * 0.5))
        elif action == "reduce_exposure":
            current = sim.graph.nodes[node_id].get("exposure", 50)
            sim.update_node_attr(node_id, exposure=max(5.0, current * 0.4))
        elif action == "reduce_criticality":
            current = sim.graph.nodes[node_id].get("criticality", 50)
            sim.update_node_attr(node_id, criticality=max(10.0, current * 0.5))
        elif action == "remove_outbound_trust":
            # Remove all outgoing edges
            outs = list(sim.graph.successors(node_id))
            for t in outs:
                sim.remove_edge(node_id, t)
        elif action == "increase_segmentation":
            # Increase distance / lower trust on edges
            for u, v, data in list(sim.graph.edges(data=True)):
                if u == node_id or v == node_id:
                    sim.graph.edges[u, v]["trust"] = max(10.0, data.get("trust", 50) * 0.5)
                    sim.graph.edges[u, v]["distance"] = data.get("distance", 1.0) * 1.5
        else:
            return {"error": f"Unknown action: {action}"}
        
        # Recompute gravity
        assets = []
        for n, data in sim.graph.nodes(data=True):
            if data.get("node_type") == "asset":
                assets.append({"id": n, **data})
        gravity_engine.compute_batch(assets)
        after_gravity_map = {a["id"]: a["gravity"] for a in assets}
        
        after_analyzer = BlastRadiusAnalyzer(sim.graph, after_gravity_map)
        after_blast = after_analyzer.compute(node_id)
        
        def pct_change(before: float, after: float) -> float:
            if before == 0:
                return 0.0
            return round(((after - before) / before) * 100.0, 1)
        
        return {
            "action": action,
            "node_id": node_id,
            "before": {
                "gravity": before_gravity.get(node_id, 0),
                "blast_score": before_blast.get("blast_score", 0),
                "reachable_count": before_blast.get("reachable_count", 0),
                "critical_exposed": len(before_blast.get("critical_assets_exposed", [])),
            },
            "after": {
                "gravity": after_gravity_map.get(node_id, 0),
                "blast_score": after_blast.get("blast_score", 0),
                "reachable_count": after_blast.get("reachable_count", 0),
                "critical_exposed": len(after_blast.get("critical_assets_exposed", [])),
            },
            "changes": {
                "gravity_pct": pct_change(
                    before_gravity.get(node_id, 0), after_gravity_map.get(node_id, 0)
                ),
                "blast_score_pct": pct_change(
                    before_blast.get("blast_score", 0), after_blast.get("blast_score", 0)
                ),
                "reachable_pct": pct_change(
                    before_blast.get("reachable_count", 0), after_blast.get("reachable_count", 0)
                ),
            },
            "note": "Modelled estimates based on the graph, not guarantees about real-world security.",
        }
