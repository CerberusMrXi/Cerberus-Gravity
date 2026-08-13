"""Unit tests for Gravity Engine."""
import pytest
from app.gravity.engine import GravityEngine, GravityWeights

def test_basic_gravity():
    engine = GravityEngine()
    g = engine.compute_gravity(
        business_value=90,
        privilege_level=80,
        reachability=40,
        trust_level=70,
        exposure=30,
        criticality=95,
    )
    assert 0 <= g <= 100
    assert g > 30  # should be reasonably high

def test_low_gravity():
    engine = GravityEngine()
    g = engine.compute_gravity(10, 10, 10, 10, 10)
    assert g < 30

def test_weights_change_result():
    e1 = GravityEngine(GravityWeights(privilege_weight=0.5))
    e2 = GravityEngine(GravityWeights(privilege_weight=2.0))
    g1 = e1.compute_gravity(50, 90, 50, 50, 50)
    g2 = e2.compute_gravity(50, 90, 50, 50, 50)
    # Different weights should produce different scores
    assert g1 != g2

def test_batch():
    engine = GravityEngine()
    assets = [
        {"id": "a1", "business_value": 80, "privilege_level": 70, "reachability": 50, "trust_level": 60, "exposure": 40},
        {"id": "a2", "business_value": 20, "privilege_level": 15, "reachability": 30, "trust_level": 20, "exposure": 10},
    ]
    engine.compute_batch(assets)
    assert "gravity" in assets[0]
    assert assets[0]["gravity"] > assets[1]["gravity"]
