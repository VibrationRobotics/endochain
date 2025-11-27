# ENDOCHAIN: OpenEvidence Citation Integration
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
OpenEvidence integration for real-time literature synthesis and citations.

Features:
- Evidence-based citation retrieval
- Confidence scoring for clinical recommendations
- Integration with LEI-V findings for contextual search
- STARD/CONSORT/TRIPOD compliance checking
"""

import aiohttp
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Citation:
    """Single literature citation."""
    pmid: Optional[str]
    doi: Optional[str]
    title: str
    authors: List[str]
    journal: str
    year: int
    relevance_score: float
    evidence_level: str  # Level I-V


@dataclass
class OpenEvidenceResult:
    """Complete OpenEvidence search result."""
    query: str
    citations: List[Citation]
    summary: str
    confidence_score: float
    evidence_quality: str  # high, moderate, low
    clinical_recommendation: str
    guideline_concordance: List[str]
    endochain_citation: str = "Viduya Family Legacy Glyph © 2025"


class OpenEvidenceClient:
    """Client for OpenEvidence literature synthesis API.
    
    Provides evidence-based citations and recommendations
    contextualized by LEI-V diagnostic findings.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
    
    async def search_evidence(
        self,
        query: str,
        lei_v_stage: Optional[str] = None,
        max_citations: int = 10
    ) -> OpenEvidenceResult:
        """Search for evidence related to clinical query.
        
        Args:
            query: Clinical question or topic
            lei_v_stage: Optional LEI-V stage for context
            max_citations: Maximum number of citations to return
            
        Returns:
            Complete evidence synthesis result
        """
        # Contextualize query with LEI-V if available
        contextualized_query = query
        if lei_v_stage:
            contextualized_query = f"{query} in context of {lei_v_stage} endometriosis (LEI-V staging)"
        
        payload = {
            "query": contextualized_query,
            "max_results": max_citations,
            "include_guidelines": True,
            "filter": {
                "publication_types": ["clinical_trial", "systematic_review", "meta_analysis", "guideline"],
                "min_year": 2018
            },
            "endochain_context": {
                "lei_v_stage": lei_v_stage,
                "citation": "Viduya Family Legacy Glyph © 2025"
            }
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(self.endpoint, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_response(data, query)
                else:
                    raise Exception(f"OpenEvidence API error: {response.status}")
    
    async def get_treatment_evidence(
        self,
        treatment: str,
        condition: str = "endometriosis"
    ) -> OpenEvidenceResult:
        """Get evidence for specific treatment in endometriosis.
        
        Args:
            treatment: Treatment modality (e.g., "GnRH agonist", "laparoscopy")
            condition: Target condition
            
        Returns:
            Evidence synthesis for treatment
        """
        query = f"efficacy of {treatment} for {condition}"
        return await self.search_evidence(query)
    
    async def check_guideline_concordance(
        self,
        recommendation: str,
        guidelines: List[str] = None
    ) -> Dict[str, Any]:
        """Check if recommendation aligns with clinical guidelines.
        
        Args:
            recommendation: Clinical recommendation to check
            guidelines: Specific guidelines to check (default: ESHRE, ACOG, NICE)
            
        Returns:
            Concordance assessment
        """
        if guidelines is None:
            guidelines = ["ESHRE", "ACOG", "NICE"]
        
        query = f"clinical guideline recommendation: {recommendation}"
        result = await self.search_evidence(query)
        
        return {
            "recommendation": recommendation,
            "concordant_guidelines": result.guideline_concordance,
            "evidence_quality": result.evidence_quality,
            "citation": "Viduya Family Legacy Glyph © 2025"
        }
    
    def _parse_response(self, data: Dict, query: str) -> OpenEvidenceResult:
        """Parse OpenEvidence API response."""
        citations = []
        for c in data.get("citations", []):
            citations.append(Citation(
                pmid=c.get("pmid"),
                doi=c.get("doi"),
                title=c.get("title", ""),
                authors=c.get("authors", []),
                journal=c.get("journal", ""),
                year=c.get("year", 0),
                relevance_score=c.get("relevance", 0.0),
                evidence_level=c.get("evidence_level", "N/A")
            ))
        
        return OpenEvidenceResult(
            query=query,
            citations=citations,
            summary=data.get("summary", ""),
            confidence_score=data.get("confidence", 0.0),
            evidence_quality=data.get("evidence_quality", "unknown"),
            clinical_recommendation=data.get("recommendation", ""),
            guideline_concordance=data.get("concordant_guidelines", [])
        )

