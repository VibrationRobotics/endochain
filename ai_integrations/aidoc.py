# ENDOCHAIN: Aidoc Radiology AI Integration
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Aidoc integration for TVUS/MRI radiology triage.

Features:
- TVUS analysis for endometrioma detection
- MRI overlay for deep infiltrating endometriosis (DIE)
- POD (Pouch of Douglas) obliteration detection (AUC 0.95)
- DICOM input with confidence scoring

Reference: Aidoc FDA-cleared AI radiology platform
"""

import aiohttp
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AidocFinding:
    """Single radiological finding from Aidoc."""
    finding_type: str
    location: str
    confidence: float
    severity: str
    dicom_reference: Optional[str]
    bounding_box: Optional[Dict[str, float]]


@dataclass
class AidocResult:
    """Complete Aidoc analysis result."""
    study_id: str
    modality: str  # TVUS, MRI
    findings: List[AidocFinding]
    pod_obliteration_score: float  # 0-1, AUC 0.95 for POD detection
    endometrioma_detected: bool
    die_indicators: List[str]
    overall_confidence: float
    processing_time_ms: int
    citation: str = "Viduya Family Legacy Glyph © 2025"


class AidocClient:
    """Client for Aidoc radiology AI API.
    
    Provides TVUS/MRI analysis with specific focus on
    endometriosis indicators including POD obliteration.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    ENDOMETRIOSIS_FINDING_TYPES = [
        "endometrioma",
        "pod_obliteration",
        "deep_infiltrating_endometriosis",
        "adhesions",
        "uterosacral_nodule",
        "rectovaginal_nodule",
        "bladder_nodule"
    ]
    
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
    
    async def analyze_study(
        self,
        dicom_reference: str,
        modality: str = "TVUS",
        lei_v_context: Optional[float] = None
    ) -> AidocResult:
        """Analyze radiology study for endometriosis indicators.
        
        Args:
            dicom_reference: DICOM study reference (PACS URI or StudyInstanceUID)
            modality: Imaging modality (TVUS or MRI)
            lei_v_context: Optional LEI-V score for context
            
        Returns:
            Complete analysis result
        """
        payload = {
            "study_reference": dicom_reference,
            "modality": modality,
            "analysis_type": "endometriosis_screening",
            "finding_types": self.ENDOMETRIOSIS_FINDING_TYPES,
            "return_bounding_boxes": True,
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
                    return self._parse_response(data, dicom_reference, modality, latency)
                else:
                    raise Exception(f"Aidoc API error: {response.status}")
    
    async def get_pod_score(
        self,
        dicom_reference: str
    ) -> float:
        """Get specific POD obliteration score.
        
        The POD (Pouch of Douglas) score indicates likelihood of
        obliteration, a key marker for deep infiltrating endometriosis.
        
        Returns:
            Score from 0.0 to 1.0 (AUC 0.95 validated)
        """
        result = await self.analyze_study(dicom_reference, modality="TVUS")
        return result.pod_obliteration_score
    
    def _parse_response(
        self,
        data: Dict,
        study_id: str,
        modality: str,
        latency: int
    ) -> AidocResult:
        """Parse Aidoc API response."""
        findings = []
        for f in data.get("findings", []):
            findings.append(AidocFinding(
                finding_type=f.get("type", "unknown"),
                location=f.get("location", ""),
                confidence=f.get("confidence", 0.0),
                severity=f.get("severity", "unknown"),
                dicom_reference=f.get("dicom_ref"),
                bounding_box=f.get("bbox")
            ))
        
        # Extract POD score
        pod_findings = [f for f in findings if f.finding_type == "pod_obliteration"]
        pod_score = pod_findings[0].confidence if pod_findings else 0.0
        
        # Check for endometrioma
        endometrioma = any(f.finding_type == "endometrioma" for f in findings)
        
        # Extract DIE indicators
        die_types = ["deep_infiltrating_endometriosis", "uterosacral_nodule", 
                     "rectovaginal_nodule", "bladder_nodule"]
        die_indicators = [f.finding_type for f in findings if f.finding_type in die_types]
        
        return AidocResult(
            study_id=study_id,
            modality=modality,
            findings=findings,
            pod_obliteration_score=pod_score,
            endometrioma_detected=endometrioma,
            die_indicators=die_indicators,
            overall_confidence=data.get("overall_confidence", 0.0),
            processing_time_ms=latency
        )

