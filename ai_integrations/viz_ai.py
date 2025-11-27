# ENDOCHAIN: Viz.ai Vascular Analysis Integration
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Viz.ai integration for vascular perfusion and deep infiltrating scoring.

Features:
- Pelvic vascular perfusion pattern analysis
- Deep infiltrating endometriosis (DIE) vascular scoring
- Neoangiogenesis detection in lesion areas
- ROI-based analysis for targeted assessment
"""

import aiohttp
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VascularROI:
    """Region of interest with vascular metrics."""
    roi_id: str
    location: str
    perfusion_index: float
    neoangiogenesis_score: float
    suspicious_for_die: bool
    bounding_coords: Dict[str, float]


@dataclass
class VizAIResult:
    """Complete Viz.ai vascular analysis result."""
    study_id: str
    overall_vascular_score: float  # 0-100
    die_likelihood: float  # 0-1
    regions_of_interest: List[VascularROI]
    perfusion_abnormalities: List[str]
    recommended_followup: str
    processing_time_ms: int
    citation: str = "Viduya Family Legacy Glyph © 2025"


class VizAIClient:
    """Client for Viz.ai vascular analysis API.
    
    Provides pelvic vascular analysis with focus on
    perfusion patterns associated with endometriosis.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
    
    async def analyze_vascular_perfusion(
        self,
        imaging_reference: str,
        modality: str = "MRI",
        lei_v_context: Optional[float] = None
    ) -> VizAIResult:
        """Analyze vascular perfusion patterns for DIE indicators.
        
        Args:
            imaging_reference: DICOM study reference
            modality: MRI (preferred) or contrast TVUS
            lei_v_context: Optional LEI-V score for context
            
        Returns:
            Complete vascular analysis result
        """
        payload = {
            "study_reference": imaging_reference,
            "modality": modality,
            "analysis_type": "pelvic_perfusion",
            "target_pathology": "endometriosis",
            "return_roi_masks": True,
            "endochain_context": {
                "lei_v": lei_v_context,
                "citation": "Viduya Family Legacy Glyph © 2025"
            }
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            start_time = datetime.utcnow()
            async with session.post(self.endpoint, json=payload, headers=headers) as response:
                latency = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                
                if response.status == 200:
                    data = await response.json()
                    return self._parse_response(data, imaging_reference, latency)
                else:
                    raise Exception(f"Viz.ai API error: {response.status}")
    
    async def get_die_score(self, imaging_reference: str) -> float:
        """Get deep infiltrating endometriosis likelihood score.
        
        Returns:
            Score from 0.0 to 1.0
        """
        result = await self.analyze_vascular_perfusion(imaging_reference)
        return result.die_likelihood
    
    def _parse_response(self, data: Dict, study_id: str, latency: int) -> VizAIResult:
        """Parse Viz.ai API response."""
        rois = []
        for r in data.get("regions_of_interest", []):
            rois.append(VascularROI(
                roi_id=r.get("id", ""),
                location=r.get("location", ""),
                perfusion_index=r.get("perfusion_index", 0.0),
                neoangiogenesis_score=r.get("neoangiogenesis", 0.0),
                suspicious_for_die=r.get("die_suspicious", False),
                bounding_coords=r.get("bounds", {})
            ))
        
        # Determine followup based on findings
        die_likelihood = data.get("die_likelihood", 0.0)
        if die_likelihood > 0.7:
            followup = "Urgent specialist referral for potential DIE"
        elif die_likelihood > 0.4:
            followup = "Specialist consultation recommended"
        else:
            followup = "Routine monitoring"
        
        return VizAIResult(
            study_id=study_id,
            overall_vascular_score=data.get("vascular_score", 0.0),
            die_likelihood=die_likelihood,
            regions_of_interest=rois,
            perfusion_abnormalities=data.get("abnormalities", []),
            recommended_followup=followup,
            processing_time_ms=latency
        )

