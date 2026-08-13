"""
CERBERUS GRAVITY Engine
=======================
Experimental Research Model for Risk-Weighted Asset Gravity.

This is NOT an industry-standard risk metric.
It is a configurable research model for studying how asset value,
privilege, reachability, trust and exposure influence attack paths.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import math

@dataclass
class GravityWeights:
    """Configurable weights for the experimental gravity model."""
    asset_value_weight: float = 1.0
    privilege_weight: float = 1.2
    reachability_weight: float = 1.0
    trust_weight: float = 0.8
    exposure_weight: float = 1.1
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "asset_value_weight": self.asset_value_weight,
            "privilege_weight": self.privilege_weight,
            "reachability_weight": self.reachability_weight,
            "trust_weight": self.trust_weight,
            "exposure_weight": self.exposure_weight,
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> "GravityWeights":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class GravityEngine:
    """
    Computes asset gravity using a configurable multi-factor model.
    
    Experimental formula (weighted sum of normalized factors + interaction term):
    
        base = Σ (w_i * factor_i) / Σ w_i
        interaction = geometric mean of factors (captures compounding risk)
        gravity = 0.65 * base + 0.35 * interaction   (then mild criticality blend)
    
    All inputs expected on 0–100 scale. Output normalized to 0–100.
    
    Clearly labeled as an experimental research model.
    """
    
    def __init__(self, weights: Optional[GravityWeights] = None):
        self.weights = weights or GravityWeights()
    
    def compute_gravity(
        self,
        business_value: float,
        privilege_level: float,
        reachability: float,
        trust_level: float,
        exposure: float,
        criticality: Optional[float] = None,
    ) -> float:
        """Compute final gravity score (0-100)."""
        w = self.weights
        factors = {
            "value": max(0.0, min(100.0, business_value)),
            "privilege": max(0.0, min(100.0, privilege_level)),
            "reachability": max(0.0, min(100.0, reachability)),
            "trust": max(0.0, min(100.0, trust_level)),
            "exposure": max(0.0, min(100.0, exposure)),
        }
        weights_map = {
            "value": w.asset_value_weight,
            "privilege": w.privilege_weight,
            "reachability": w.reachability_weight,
            "trust": w.trust_weight,
            "exposure": w.exposure_weight,
        }
        
        # Weighted arithmetic mean
        total_w = sum(weights_map.values()) or 1.0
        base = sum(factors[k] * weights_map[k] for k in factors) / total_w
        
        # Geometric mean (compounding) — avoid zeros
        geo_product = 1.0
        for k in factors:
            geo_product *= max(factors[k] / 100.0, 0.01) ** (weights_map[k] / total_w)
        interaction = (geo_product ** 1.0) * 100.0
        
        gravity = 0.65 * base + 0.35 * interaction
        
        if criticality is not None:
            crit = max(0.0, min(100.0, criticality))
            gravity = 0.80 * gravity + 0.20 * crit
        
        return round(max(0.0, min(100.0, gravity)), 2)
    
    def compute_batch(self, assets: list) -> list:
        """Compute gravity for a list of asset dicts. Mutates and returns them."""
        for asset in assets:
            asset["gravity"] = self.compute_gravity(
                business_value=asset.get("business_value", 50.0),
                privilege_level=asset.get("privilege_level", 30.0),
                reachability=asset.get("reachability", 40.0),
                trust_level=asset.get("trust_level", 50.0),
                exposure=asset.get("exposure", 30.0),
                criticality=asset.get("criticality"),
            )
        return assets
    
    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """Update model weights from dict."""
        self.weights = GravityWeights.from_dict({**self.weights.to_dict(), **new_weights})
