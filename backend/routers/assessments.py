# ENDOCHAIN Backend: Assessment Endpoints
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
RESTful endpoints for LEI-V diagnostic assessments.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
import uuid

router = APIRouter()


class EVGReading(BaseModel):
    """Single EVG electrode reading."""
    electrode_index: int = Field(..., ge=1, le=6, description="RSL electrode 1-6")
    radial_distance: float = Field(..., description="Radial distance from glyph center")
    impedance: Optional[float] = Field(None, description="Electrode impedance (Ω)")
    timestamp: datetime


class AssessmentRequest(BaseModel):
    """Request for LEI-V diagnostic assessment."""
    patient_id: str = Field(..., description="Anonymized patient identifier")
    evg_readings: List[EVGReading] = Field(..., min_length=6, max_length=6)
    cycle_day: Optional[int] = Field(None, ge=1, le=35, description="Menstrual cycle day")
    v_caw_hour: Optional[int] = Field(None, ge=0, le=96, description="Hour in V-CAW window")
    clinical_notes: Optional[str] = Field(None, description="Optional clinical notes")
    request_ai_fusion: bool = Field(True, description="Request multi-platform AI analysis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "ENDO-2025-001",
                "evg_readings": [
                    {"electrode_index": 1, "radial_distance": 0.433, "impedance": 1200, "timestamp": "2025-11-26T10:00:00Z"},
                    {"electrode_index": 2, "radial_distance": 0.435, "impedance": 1180, "timestamp": "2025-11-26T10:00:00Z"},
                    {"electrode_index": 3, "radial_distance": 0.431, "impedance": 1220, "timestamp": "2025-11-26T10:00:00Z"},
                    {"electrode_index": 4, "radial_distance": 0.434, "impedance": 1190, "timestamp": "2025-11-26T10:00:00Z"},
                    {"electrode_index": 5, "radial_distance": 0.432, "impedance": 1210, "timestamp": "2025-11-26T10:00:00Z"},
                    {"electrode_index": 6, "radial_distance": 0.433, "impedance": 1195, "timestamp": "2025-11-26T10:00:00Z"}
                ],
                "cycle_day": 14,
                "v_caw_hour": 48,
                "request_ai_fusion": True
            }
        }


class AssessmentResponse(BaseModel):
    """LEI-V diagnostic assessment result."""
    assessment_id: str
    patient_id: str
    lei_v: float
    lei_v_symbolic: str
    stage: str
    confidence_percent: float
    platform_results: Optional[Dict[str, Any]]
    ensemble_consensus: Optional[Dict[str, Any]]
    next_steps: List[str]
    timestamp: datetime
    audit_hash: str
    citation: str = "Viduya Family Legacy Glyph © 2025"


@router.post("/", response_model=AssessmentResponse)
async def create_assessment(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks
):
    """Create new LEI-V diagnostic assessment.
    
    Computes LEI-V from 6 EVG electrode readings using exact symbolic
    mathematics. Optionally triggers multi-platform AI fusion analysis.
    
    **Citation:** Viduya Family Legacy Glyph © 2025
    """
    import sympy as sp
    from core.lei_v import LEIVCalculator
    
    # Convert readings to symbolic radial distances
    radial_distances = [
        sp.Rational(str(r.radial_distance)) 
        for r in sorted(request.evg_readings, key=lambda x: x.electrode_index)
    ]
    
    # Compute LEI-V
    calculator = LEIVCalculator()
    result = calculator.compute(
        radial_distances=radial_distances,
        patient_id=request.patient_id,
        cycle_day=request.cycle_day,
        v_caw_hour=request.v_caw_hour
    )
    
    # Determine next steps based on stage
    next_steps = _get_next_steps(result.stage.value, result.confidence_percent)
    
    # Build response
    response = AssessmentResponse(
        assessment_id=str(uuid.uuid4()),
        patient_id=request.patient_id,
        lei_v=float(result.lei_v_value),
        lei_v_symbolic=str(result.lei_v_symbolic),
        stage=result.stage.value,
        confidence_percent=result.confidence_percent,
        platform_results=None,
        ensemble_consensus=None,
        next_steps=next_steps,
        timestamp=result.timestamp,
        audit_hash=result.audit_hash
    )
    
    # Queue AI fusion if requested
    if request.request_ai_fusion:
        background_tasks.add_task(_run_ai_fusion, response.assessment_id, request)
    
    return response


def _get_next_steps(stage: str, confidence: float) -> List[str]:
    """Generate clinical next steps based on LEI-V stage."""
    steps = []
    if stage == "healthy":
        steps = ["Continue routine monitoring", "Annual follow-up recommended"]
    elif stage == "stage_0_early":
        steps = [
            "96-hour V-CAW EVG confirmation",
            "Saliva miRNA panel (selected biomarkers)",
            "Gynecology specialist referral",
            "Consider medical management trial"
        ]
    else:
        steps = [
            "Immediate specialist referral",
            "TVUS/MRI imaging recommended",
            "Laparoscopic evaluation discussion",
            "Pain management consultation"
        ]
    
    if confidence < 80:
        steps.insert(0, "Repeat assessment recommended (low confidence)")
    
    return steps


async def _run_ai_fusion(assessment_id: str, request: AssessmentRequest):
    """Background task for multi-platform AI fusion."""
    # This would call the AI orchestration service
    pass


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: str):
    """Retrieve completed assessment by ID."""
    raise HTTPException(status_code=404, detail="Assessment not found")

