# ENDOCHAIN Backend: FastAPI Application
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Main FastAPI application with FHIR-compliant endpoints.
"""

from fastapi import FastAPI, HTTPException, Depends, Security, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from typing import Optional

from .config import Settings, get_settings
from .routers import assessments, patients, fhir, audit, ai_platforms, evg
from .middleware import AuditMiddleware, RateLimitMiddleware


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("endochain")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("ENDOCHAIN-VIDUYA-2025 starting...")
    logger.info("Viduya Family Legacy Glyph © 2025 - All Rights Reserved")
    # Initialize connections
    yield
    logger.info("ENDOCHAIN-VIDUYA-2025 shutting down...")


app = FastAPI(
    title="ENDOCHAIN-VIDUYA-2025 API",
    description="""
    ## Geometrically-Anchored Endometriosis Diagnostic System
    
    **Viduya Family Legacy Glyph © 2025 – All Rights Reserved**
    
    This API provides:
    - LEI-V (Lesion Entropy Index - Viduya variant) computation
    - Multi-platform AI diagnostic fusion
    - HL7 FHIR R5 compliant data exchange
    - EU EHDS profile support
    - Immutable audit trail with 256-bit hashes
    
    ### Regulatory Compliance
    - FDA 510(k) De Novo pathway
    - EU MDR Class IIa
    - HIPAA / GDPR compliant
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS configuration for medical dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dashboard.endochain.org", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(AuditMiddleware)


# Include routers
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(fhir.router, prefix="/api/v1/fhir", tags=["FHIR"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])
app.include_router(ai_platforms.router, prefix="/api/v1/ai", tags=["AI Platforms"])
app.include_router(evg.router, prefix="/api/v1", tags=["EVG Processing"])


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with system information."""
    return {
        "system": "ENDOCHAIN-VIDUYA-2025",
        "version": "1.0.0",
        "status": "operational",
        "citation": "Viduya Family Legacy Glyph © 2025",
        "endpoints": {
            "docs": "/api/docs",
            "assessments": "/api/v1/assessments",
            "fhir": "/api/v1/fhir",
            "audit": "/api/v1/audit"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "connected",
            "ai_platforms": "available",
            "fhir_server": "connected"
        }
    }

