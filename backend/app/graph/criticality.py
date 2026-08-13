"""
Criticality Analysis combining Graph Theory + Gravity
====================================================
Clearly separates graph-theoretic metrics from CERBERUS experimental gravity.
"""
from typing import Dict, List, Any, Optional
import networkx as nx

class CriticalityAnalyzer:
    """Computes centrality metrics and strategic criticality."""
    
    def __init__(self, graph: nx.DiGraph, gravity_map: Dict[str, float]):
        self.graph = graph
        self.gravity_map = gravity_map
    
    def compute_centralities(self) -> Dict[str, Dict[str, float]]:
        """Compute standard graph-theoretic centralities."""
        if self.graph.number_of_nodes() == 0:
            return {}
        
        # Undirected version for some metrics
        undirected = self.graph.to_undirected()
        
        degree = dict(nx.degree_centrality(self.graph))
        try:
            betweenness = dict(nx.betweenness_centrality(self.graph, normalized=True))
        except Exception:
            betweenness = {n: 0.0 for n in self.graph.nodes()}
        
        try:
            closeness = dict(nx.closeness_centrality(undirected))
        except Exception:
            closeness = {n: 0.0 for n in self.graph.nodes()}
        
        try:
            pagerank = dict(nx.pagerank(self.graph, alpha=0.85))
        except Exception:
            pagerank = {n: 0.0 for n in self.graph.nodes()}
        
        try:
            eigenvector = dict(nx.eigenvector_centrality(undirected, max_iter=500))
        except Exception:
            eigenvector = {n: 0.0 for n in self.graph.nodes()}
        
        result = {}
        for node in self.graph.nodes():
            result[node] = {
                "degree_centrality": round(degree.get(node, 0.0), 4),
                "betweenness_centrality": round(betweenness.get(node, 0.0), 4),
                "closeness_centrality": round(closeness.get(node, 0.0), 4),
                "pagerank": round(pagerank.get(node, 0.0), 4),
                "eigenvector_centrality": round(eigenvector.get(node, 0.0), 4),
            }
        return result
    
    def strategic_criticality(
        self,
        centralities: Optional[Dict[str, Dict[str, float]]] = None,
        gravity_weight: float = 0.45,
        betweenness_weight: float = 0.25,
        pagerank_weight: float = 0.15,
        degree_weight: float = 0.15,
    ) -> Dict[str, float]:
        """
        Strategic Criticality Score (experimental).
        Combines gravity with graph-theoretic metrics.
        
        Clearly labeled as CERBERUS experimental metric.
        """
        if centralities is None:
            centralities = self.compute_centralities()
        
        scores = {}
        for node in self.graph.nodes():
            g = self.gravity_map.get(node, 0.0) / 100.0
            c = centralities.get(node, {})
            score = (
                gravity_weight * g +
                betweenness_weight * c.get("betweenness_centrality", 0.0) +
                pagerank_weight * c.get("pagerank", 0.0) +
                degree_weight * c.get("degree_centrality", 0.0)
            ) * 100.0
            scores[node] = round(score, 2)
        return scores
    
    def detect_gravity_wells(
        self,
        threshold: float = 70.0,
        cluster_distance: int = 2,
    ) -> Dict[str, Any]:
        """
        Detect single-node and multi-node gravity wells.
        """
        high = {n: g for n, g in self.gravity_map.items() if g >= threshold}
        
        single_wells = []
        multi_wells = []
        
        visited = set()
        for node, g in sorted(high.items(), key=lambda x: -x[1]):
            if node in visited:
                continue
            # Find nearby high-gravity nodes
            try:
                nearby = set(nx.single_source_shortest_path_length(
                    self.graph.to_undirected(), node, cutoff=cluster_distance
                ).keys())
            except Exception:
                nearby = {node}
            
            cluster = [n for n in nearby if n in high]
            for n in cluster:
                visited.add(n)
            
            if len(cluster) == 1:
                single_wells.append({"nodes": cluster, "max_gravity": g})
            else:
                multi_wells.append({
                    "nodes": cluster,
                    "max_gravity": max(self.gravity_map.get(n, 0) for n in cluster),
                    "avg_gravity": round(
                        sum(self.gravity_map.get(n, 0) for n in cluster) / len(cluster), 2
                    ),
                })
        
        return {
            "single_node_wells": single_wells,
            "multi_node_wells": multi_wells,
            "total_wells": len(single_wells) + len(multi_wells),
            "threshold": threshold,
        }
