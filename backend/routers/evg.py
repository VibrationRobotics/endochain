# ENDOCHAIN-VIDUYA-2025 - EVG Processing Router
# Viduya Family Legacy Glyph (C) 2025 - All Rights Reserved
"""
API endpoints for EVG file processing and LEI-V computation.
"""

import os
import tempfile
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.edf_processor import process_patient_edf
from core.viduya_constants import CITATION


router = APIRouter(prefix="/evg", tags=["EVG Processing"])


class EVGProcessingResponse(BaseModel):
    """Response model for EVG processing."""
    status: str
    processing_time_seconds: float
    under_3_minutes: bool
    patient_id: str
    recording_date: str
    duration_hours: float
    lei_v: float
    lei_v_symbolic: str
    stage: str
    confidence_percent: float
    radial_distances: list[float]
    mean_radial: float
    audit_hash: str
    bitcoin_timestamp_payload: str
    file_hash: str
    timestamp: str
    citation: str


async def send_report_email(result: dict, email: str):
    """Background task to send report via email."""
    # TODO: Implement email sending
    print(f"Would send report to {email}")
    print(f"LEI-V: {result['lei_v']}, Stage: {result['stage']}")


@router.post("/process", response_model=EVGProcessingResponse)
async def process_evg_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    notify_email: Optional[str] = None
):
    """
    Process a 96-hour EVG .edf file and compute LEI-V.
    
    This is the main endpoint for clinical processing.
    Target: Complete in under 3 minutes.
    
    Returns:
        Complete processing result with audit hash and Bitcoin timestamp payload.
    """
    if not file.filename.endswith('.edf'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a .edf file."
        )
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.edf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Process the file
        result = process_patient_edf(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Schedule email notification if requested
        if notify_email and background_tasks:
            background_tasks.add_task(send_report_email, result, notify_email)
        
        return EVGProcessingResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}"
        )


@router.get("/status")
async def get_processing_status():
    """Check if the EVG processing service is ready."""
    return {
        "status": "ready",
        "version": "1.0.0-clinical-ready",
        "citation": CITATION,
        "target_processing_time": "< 3 minutes",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/thresholds")
async def get_leiv_thresholds():
    """Return the official LEI-V clinical thresholds."""
    return {
        "healthy": {"min": 0, "max": 0.018, "description": "No evidence of endometriosis"},
        "stage_0": {"min": 0.018, "max": 0.08, "description": "Early/molecular stage"},
        "stage_1_2": {"min": 0.08, "max": 0.25, "description": "Minimal to mild"},
        "stage_3_4": {"min": 0.25, "max": 1.0, "description": "Moderate to severe"},
        "citation": CITATION
    }

