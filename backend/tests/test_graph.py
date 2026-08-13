"""Graph engine tests."""
import pytest
from app.graph.engine import GraphEngine
from app.gravity.engine import GravityEngine

SAMPLE = {
    "assets": [
        {"id": "a", "name": "A", "type": "server", "criticality": 50, "privilege_level": 40, "reachability": 60, "exposure": 30, "trust_level": 50, "business_value": 50},
        {"id": "b", "name": "B", "type": "server", "criticality": 80, "privilege_level": 70, "reachability": 40, "exposure": 20, "trust_level": 70, "business_value": 80},
    ],
    "relationships": [
        {"source": "a", "target": "b", "relationship_type": "access", "trust": 60, "permission": "ssh", "distance": 1.0, "confidence": 0.9}
    ]
}

def test_load_graph():
    ge = GraphEngine()
    ge.load_from_dict(SAMPLE)
    assert ge.graph.number_of_nodes() == 2
    assert ge.graph.number_of_edges() == 1

def test_gravity_on_graph():
    ge = GraphEngine()
    ge.load_from_dict(SAMPLE)
    engine = GravityEngine()
    assets = [{"id": n, **d} for n, d in ge.graph.nodes(data=True)]
    engine.compute_batch(assets)
    for a in assets:
        ge.update_node_attr(a["id"], gravity=a["gravity"])
    gmap = {n: d["gravity"] for n, d in ge.graph.nodes(data=True)}
    assert gmap["b"] > gmap["a"]
