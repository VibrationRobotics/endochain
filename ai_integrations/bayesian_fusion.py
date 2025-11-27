# ENDOCHAIN: Bayesian Fusion Engine
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Bayesian fusion engine for multi-platform AI confidence scoring.

The fusion uses LEI-V as the geometric anchor, weighting platform
contributions based on their concordance with the LEI-V stage.

Mathematical Foundation:
P(Diagnosis|LEI-V, Platforms) ∝ P(LEI-V|Diagnosis) × Π P(Platform_i|Diagnosis)

Citation: Viduya Family Legacy Glyph © 2025
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from decimal import Decimal
import math

from core.audit import AuditHasher


@dataclass
class PlatformContribution:
    """Contribution of single platform to fusion."""
    platform: str
    raw_confidence: float
    concordance_with_leiv: float
    adjusted_weight: float
    contribution_to_final: float


@dataclass
class FusionResult:
    """Complete Bayesian fusion result."""
    final_confidence: float
    final_diagnosis: str
    lei_v_anchor_contribution: float
    platform_contributions: List[PlatformContribution]
    prior_probability: float
    posterior_probability: float
    evidence_strength: str  # strong, moderate, weak
    audit_hash: str
    citation: str = "Viduya Family Legacy Glyph © 2025"


class BayesianFusionEngine:
    """Bayesian fusion engine with LEI-V geometric anchoring.
    
    All platform outputs are fused using Bayesian inference with
    LEI-V serving as the prior distribution anchor.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    # Prior probabilities for endometriosis by LEI-V stage
    STAGE_PRIORS = {
        "healthy": 0.05,
        "stage_0_early": 0.70,
        "stage_i_minimal": 0.85,
        "stage_ii_mild": 0.90,
        "stage_iii_moderate": 0.95,
        "stage_iv_severe": 0.98
    }
    
    # Platform reliability weights (based on validation studies)
    PLATFORM_RELIABILITY = {
        "med_gemini": 0.85,
        "aidoc": 0.90,  # AUC 0.95 for POD
        "tempus": 0.75,
        "viz_ai": 0.80,
        "openevidence": 0.70
    }
    
    def __init__(self):
        self.hasher = AuditHasher()
    
    def fuse(
        self,
        lei_v_value: float,
        lei_v_stage: str,
        lei_v_confidence: float,
        platform_results: List[Dict[str, Any]]
    ) -> FusionResult:
        """Perform Bayesian fusion of LEI-V and platform results.
        
        Args:
            lei_v_value: Computed LEI-V value
            lei_v_stage: Classified stage from LEI-V
            lei_v_confidence: Confidence from LEI-V calculation
            platform_results: List of platform result dictionaries
            
        Returns:
            Complete fusion result with audit trail
        """
        # Get prior based on LEI-V stage
        prior = self.STAGE_PRIORS.get(lei_v_stage, 0.5)
        
        # Calculate LEI-V anchor contribution
        lei_v_weight = self._calculate_leiv_weight(lei_v_value, lei_v_confidence)
        lei_v_contribution = prior * lei_v_weight
        
        # Process each platform's contribution
        contributions = []
        likelihood_product = 1.0
        
        for result in platform_results:
            platform = result.get("platform", "unknown")
            raw_conf = result.get("confidence", 0.0) / 100.0
            
            # Calculate concordance with LEI-V
            concordance = self._calculate_concordance(
                platform, result, lei_v_stage
            )
            
            # Adjust weight based on reliability and concordance
            reliability = self.PLATFORM_RELIABILITY.get(platform, 0.5)
            adjusted_weight = reliability * concordance
            
            # Contribution to likelihood
            platform_likelihood = raw_conf * adjusted_weight
            likelihood_product *= (1 + platform_likelihood)
            
            contributions.append(PlatformContribution(
                platform=platform,
                raw_confidence=raw_conf * 100,
                concordance_with_leiv=concordance,
                adjusted_weight=adjusted_weight,
                contribution_to_final=platform_likelihood
            ))
        
        # Bayesian posterior calculation
        # P(D|E) = P(E|D) × P(D) / P(E)
        # Simplified: posterior ∝ likelihood × prior
        unnormalized_posterior = lei_v_contribution * likelihood_product
        
        # Normalize to 0-1 range
        posterior = min(0.99, unnormalized_posterior / (unnormalized_posterior + 0.1))
        
        # Convert to percentage and determine diagnosis
        final_confidence = posterior * 100
        final_diagnosis = self._determine_diagnosis(lei_v_stage, posterior)
        
        # Determine evidence strength
        if len(contributions) >= 3 and all(c.concordance_with_leiv > 0.7 for c in contributions):
            evidence_strength = "strong"
        elif len(contributions) >= 2 and posterior > 0.75:
            evidence_strength = "moderate"
        else:
            evidence_strength = "weak"
        
        # Generate audit hash
        audit_data = {
            "lei_v": lei_v_value,
            "lei_v_stage": lei_v_stage,
            "posterior": posterior,
            "platforms": [c.platform for c in contributions]
        }
        audit_hash = self.hasher.hash_computation(audit_data)
        
        return FusionResult(
            final_confidence=final_confidence,
            final_diagnosis=final_diagnosis,
            lei_v_anchor_contribution=lei_v_contribution,
            platform_contributions=contributions,
            prior_probability=prior,
            posterior_probability=posterior,
            evidence_strength=evidence_strength,
            audit_hash=audit_hash
        )
    
    def _calculate_leiv_weight(self, lei_v: float, confidence: float) -> float:
        """Calculate LEI-V anchor weight based on value and confidence."""
        # Higher weight for values far from thresholds (clear classification)
        threshold_distance = min(
            abs(lei_v - 0.018),  # Distance from Stage-0 threshold
            abs(lei_v - 0.08)   # Distance from advanced threshold
        )
        clarity_factor = min(1.0, threshold_distance * 20)
        
        return (confidence / 100) * (0.5 + 0.5 * clarity_factor)
    
    def _calculate_concordance(
        self,
        platform: str,
        result: Dict,
        lei_v_stage: str
    ) -> float:
        """Calculate concordance between platform result and LEI-V stage."""
        # Platform-specific concordance logic
        platform_stage = result.get("stage", result.get("classification", ""))
        
        if not platform_stage:
            return 0.5  # Neutral if no stage info
        
        # Simple concordance: same severity = high, adjacent = medium, else low
        lei_v_severity = self._get_severity_level(lei_v_stage)
        platform_severity = self._get_severity_level(platform_stage)
        
        diff = abs(lei_v_severity - platform_severity)
        if diff == 0:
            return 1.0
        elif diff == 1:
            return 0.7
        elif diff == 2:
            return 0.4
        else:
            return 0.2
    
    def _get_severity_level(self, stage: str) -> int:
        """Map stage to numeric severity level."""
        stage_lower = stage.lower()
        if "healthy" in stage_lower or "normal" in stage_lower:
            return 0
        elif "stage_0" in stage_lower or "early" in stage_lower or "minimal" in stage_lower:
            return 1
        elif "stage_i" in stage_lower or "mild" in stage_lower:
            return 2
        elif "stage_ii" in stage_lower or "moderate" in stage_lower:
            return 3
        elif "stage_iii" in stage_lower or "stage_iv" in stage_lower or "severe" in stage_lower:
            return 4
        return 2  # Default to middle
    
    def _determine_diagnosis(self, lei_v_stage: str, posterior: float) -> str:
        """Determine final diagnosis string."""
        confidence_qualifier = "high" if posterior > 0.85 else "moderate" if posterior > 0.70 else "low"
        return f"{lei_v_stage.replace('_', ' ').title()} ({confidence_qualifier} confidence) - LEI-V anchored"

