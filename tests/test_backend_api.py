# ENDOCHAIN Tests: Backend API
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Integration tests for FastAPI backend.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    @pytest.fixture
    def client(self):
        # Import here to avoid circular imports
        from backend.main import app
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Root should return system info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["system"] == "ENDOCHAIN-VIDUYA-2025"
        assert "citation" in data
        assert "Viduya" in data["citation"]
    
    def test_health_endpoint(self, client):
        """Health check should return healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestAssessmentEndpoints:
    """Tests for assessment API endpoints."""
    
    @pytest.fixture
    def client(self):
        from backend.main import app
        return TestClient(app)
    
    @pytest.fixture
    def valid_assessment_request(self):
        """Valid assessment request payload."""
        return {
            "patient_id": "TEST-2025-001",
            "evg_readings": [
                {
                    "electrode_index": i,
                    "radial_distance": 0.433 + (i - 3) * 0.001,
                    "impedance": 1200,
                    "timestamp": datetime.utcnow().isoformat()
                }
                for i in range(1, 7)
            ],
            "cycle_day": 14,
            "v_caw_hour": 48,
            "request_ai_fusion": False
        }
    
    def test_create_assessment(self, client, valid_assessment_request):
        """Should create assessment and return LEI-V result."""
        response = client.post(
            "/api/v1/assessments/",
            json=valid_assessment_request
        )
        assert response.status_code == 200
        data = response.json()
        assert "lei_v" in data
        assert "stage" in data
        assert "audit_hash" in data
        assert data["patient_id"] == "TEST-2025-001"
    
    def test_assessment_includes_citation(self, client, valid_assessment_request):
        """Assessment response should include citation."""
        response = client.post(
            "/api/v1/assessments/",
            json=valid_assessment_request
        )
        data = response.json()
        assert "citation" in data
        assert "Viduya" in data["citation"]
    
    def test_assessment_requires_six_electrodes(self, client):
        """Should reject requests without 6 electrodes."""
        invalid_request = {
            "patient_id": "TEST-2025-002",
            "evg_readings": [
                {"electrode_index": 1, "radial_distance": 0.433, 
                 "timestamp": datetime.utcnow().isoformat()}
            ] * 5,  # Only 5 electrodes
            "request_ai_fusion": False
        }
        response = client.post(
            "/api/v1/assessments/",
            json=invalid_request
        )
        assert response.status_code == 422  # Validation error


class TestFHIREndpoints:
    """Tests for FHIR API endpoints."""
    
    @pytest.fixture
    def client(self):
        from backend.main import app
        return TestClient(app)
    
    def test_validate_observation(self, client):
        """Should validate FHIR Observation resource."""
        observation = {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{"system": "http://endochain.org", "code": "VIDUYA-LEI-V"}]
            },
            "subject": {"reference": "Patient/123"}
        }
        response = client.post("/api/v1/fhir/validate", json=observation)
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == True
    
    def test_validate_missing_required_field(self, client):
        """Should return error for missing required fields."""
        invalid_observation = {
            "resourceType": "Observation",
            "status": "final"
            # Missing code and subject
        }
        response = client.post("/api/v1/fhir/validate", json=invalid_observation)
        data = response.json()
        assert data["valid"] == False
        assert len(data["errors"]) > 0


class TestAuditEndpoints:
    """Tests for audit API endpoints."""
    
    @pytest.fixture
    def client(self):
        from backend.main import app
        return TestClient(app)
    
    def test_verify_chain(self, client):
        """Should verify audit chain integrity."""
        response = client.get("/api/v1/audit/verify")
        assert response.status_code == 200
        data = response.json()
        assert "chain_intact" in data
    
    def test_get_audit_logs(self, client):
        """Should return audit logs."""
        response = client.get("/api/v1/audit/logs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

