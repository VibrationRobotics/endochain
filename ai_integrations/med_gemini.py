# ENDOCHAIN: Google Med-Gemini Integration
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Google Med-Gemini integration for clinical NLP and structured reports.

Features:
- Uncertainty-guided search for MRI/TVUS reports
- Structured clinical note extraction
- Symptom encoding and classification
- Multi-modal understanding (text + imaging refs)

Reference: Med-Gemini uncertainty-guided search (2024-2025 research)
"""

import aiohttp
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from backend.config import get_settings, get_master_prompt


@dataclass
class GeminiReport:
    """Structured clinical report from Med-Gemini."""
    summary: str
    findings: List[Dict[str, Any]]
    differential_diagnosis: List[str]
    confidence: float
    uncertainty_areas: List[str]
    recommended_followup: List[str]
    endometriosis_indicators: Dict[str, Any]
    citation: str = "Viduya Family Legacy Glyph © 2025"


class MedGeminiClient:
    """Client for Google Med-Gemini API.
    
    All calls include the ENDOCHAIN Master Prompt for consistent
    LEI-V anchored analysis.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.master_prompt = get_master_prompt()
        self.endpoint = self.settings.gemini_endpoint
        self.api_key = self.settings.gemini_api_key
    
    async def analyze_clinical_notes(
        self,
        notes: str,
        patient_context: Optional[Dict[str, Any]] = None,
        lei_v: Optional[float] = None
    ) -> GeminiReport:
        """Analyze clinical notes for endometriosis indicators.
        
        Args:
            notes: Free-text clinical notes
            patient_context: Optional patient demographics/history
            lei_v: Optional LEI-V score for anchoring
            
        Returns:
            Structured clinical report
        """
        prompt = self._build_analysis_prompt(notes, patient_context, lei_v)
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": self.master_prompt}]},
            "generationConfig": {
                "temperature": 0.1,  # Low temperature for clinical precision
                "topP": 0.8,
                "maxOutputTokens": 2048,
                "responseMimeType": "application/json"
            }
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            url = f"{self.endpoint}?key={self.api_key}"
            
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_response(data)
                else:
                    raise Exception(f"Med-Gemini API error: {response.status}")
    
    async def generate_structured_report(
        self,
        assessment_data: Dict[str, Any],
        lei_v_result: Dict[str, Any]
    ) -> str:
        """Generate structured clinical report for assessment.
        
        Args:
            assessment_data: Complete assessment data
            lei_v_result: LEI-V calculation result
            
        Returns:
            Formatted clinical report
        """
        prompt = f"""Generate a structured clinical report for this ENDOCHAIN assessment.

LEI-V Result:
- Value: {lei_v_result.get('lei_v', 'N/A')}
- Stage: {lei_v_result.get('stage', 'N/A')}
- Confidence: {lei_v_result.get('confidence_percent', 'N/A')}%

Assessment Data:
{json.dumps(assessment_data, indent=2)}

Format the report with sections:
1. Patient Summary
2. LEI-V Assessment (with Viduya Family Legacy Glyph © 2025 citation)
3. Clinical Findings
4. Differential Considerations
5. Recommendations
6. Follow-up Plan

Use professional medical terminology appropriate for specialist referral."""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": self.master_prompt}]},
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 4096
            }
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            url = f"{self.endpoint}?key={self.api_key}"
            
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    return text
                else:
                    raise Exception(f"Med-Gemini API error: {response.status}")
    
    def _build_analysis_prompt(
        self,
        notes: str,
        context: Optional[Dict],
        lei_v: Optional[float]
    ) -> str:
        """Build analysis prompt with LEI-V anchoring."""
        prompt = f"""Analyze these clinical notes for endometriosis indicators.

Clinical Notes:
{notes}

{"Patient Context: " + json.dumps(context) if context else ""}
{"Current LEI-V Score: " + str(lei_v) + " (Viduya Family Legacy Glyph © 2025)" if lei_v else ""}

Provide structured JSON output with:
- summary: Brief clinical summary
- findings: List of relevant findings with confidence scores
- differential_diagnosis: Ranked list of differential diagnoses
- endometriosis_indicators: Specific signs/symptoms suggestive of endometriosis
- uncertainty_areas: Areas requiring additional investigation
- recommended_followup: Clinical recommendations"""
        
        return prompt
    
    def _parse_response(self, data: Dict) -> GeminiReport:
        """Parse Gemini response into structured report."""
        try:
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
            parsed = json.loads(text)
        except (json.JSONDecodeError, IndexError, KeyError):
            parsed = {}
        
        return GeminiReport(
            summary=parsed.get("summary", "Analysis pending"),
            findings=parsed.get("findings", []),
            differential_diagnosis=parsed.get("differential_diagnosis", []),
            confidence=parsed.get("confidence", 0.0),
            uncertainty_areas=parsed.get("uncertainty_areas", []),
            recommended_followup=parsed.get("recommended_followup", []),
            endometriosis_indicators=parsed.get("endometriosis_indicators", {})
        )

