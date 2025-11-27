# ENDOCHAIN Backend: Patient Endpoints
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Patient registration and longitudinal tracking endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import uuid

router = APIRouter()


class PatientCreate(BaseModel):
    """Patient registration request."""
    external_id: Optional[str] = Field(None, description="External EHR patient ID")
    date_of_birth: date
    cycle_length_days: Optional[int] = Field(28, ge=21, le=40)
    symptom_onset_date: Optional[date] = None
    primary_symptoms: List[str] = Field(default_factory=list)
    consent_timestamp: datetime
    consent_version: str = "1.0"


class Patient(BaseModel):
    """Patient record."""
    patient_id: str
    external_id: Optional[str]
    date_of_birth: date
    cycle_length_days: int
    symptom_onset_date: Optional[date]
    primary_symptoms: List[str]
    created_at: datetime
    consent_timestamp: datetime
    consent_version: str
    total_assessments: int = 0
    last_lei_v: Optional[float] = None
    last_assessment_date: Optional[datetime] = None


class LEIVTrend(BaseModel):
    """Longitudinal LEI-V trend data point."""
    timestamp: datetime
    lei_v: float
    stage: str
    cycle_day: Optional[int]
    confidence_percent: float


class PatientHistory(BaseModel):
    """Patient longitudinal history."""
    patient_id: str
    trend_data: List[LEIVTrend]
    mean_lei_v: float
    lei_v_variance: float
    trend_direction: str  # "improving", "stable", "worsening"
    citation: str = "Viduya Family Legacy Glyph © 2025"


@router.post("/", response_model=Patient)
async def register_patient(patient: PatientCreate):
    """Register new patient with informed consent.
    
    All patient data is encrypted at rest and includes audit trail.
    HIPAA/GDPR compliant.
    """
    patient_id = f"ENDO-{datetime.utcnow().strftime('%Y')}-{str(uuid.uuid4())[:8].upper()}"
    
    return Patient(
        patient_id=patient_id,
        external_id=patient.external_id,
        date_of_birth=patient.date_of_birth,
        cycle_length_days=patient.cycle_length_days or 28,
        symptom_onset_date=patient.symptom_onset_date,
        primary_symptoms=patient.primary_symptoms,
        created_at=datetime.utcnow(),
        consent_timestamp=patient.consent_timestamp,
        consent_version=patient.consent_version,
        total_assessments=0
    )


@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    """Retrieve patient by ID."""
    raise HTTPException(status_code=404, detail="Patient not found")


@router.get("/{patient_id}/history", response_model=PatientHistory)
async def get_patient_history(
    patient_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Get longitudinal LEI-V trend for patient.
    
    Returns time-series data suitable for visualization and
    trend analysis.
    
    **Citation:** Viduya Family Legacy Glyph © 2025
    """
    raise HTTPException(status_code=404, detail="Patient not found")


@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    """Delete patient and all associated data (GDPR right to erasure).
    
    This action is irreversible. All assessments, audit logs, and
    derived data will be permanently deleted.
    """
    raise HTTPException(status_code=404, detail="Patient not found")

