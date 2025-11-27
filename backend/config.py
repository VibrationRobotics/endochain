# ENDOCHAIN Backend: Configuration
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Application configuration with environment variable support.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "ENDOCHAIN-VIDUYA-2025"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # FHIR Server
    fhir_base_url: str = Field(default="http://localhost:8080/fhir", env="FHIR_BASE_URL")
    fhir_version: str = "R5"
    
    # AI Platform API Keys
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    aidoc_api_key: Optional[str] = Field(default=None, env="AIDOC_API_KEY")
    tempus_api_key: Optional[str] = Field(default=None, env="TEMPUS_API_KEY")
    viz_ai_api_key: Optional[str] = Field(default=None, env="VIZ_AI_API_KEY")
    openevidence_api_key: Optional[str] = Field(default=None, env="OPENEVIDENCE_API_KEY")
    
    # AI Platform Endpoints
    gemini_endpoint: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
    aidoc_endpoint: str = "https://api.aidoc.com/v1/detect"
    tempus_endpoint: str = "https://api.tempus.com/v3/insights"
    viz_ai_endpoint: str = "https://api.viz.ai/v1/analyze"
    openevidence_endpoint: str = "https://api.openevidence.com/v1/search"
    
    # OpenBCI / EVG Hardware
    openbci_serial_port: str = Field(default="/dev/ttyUSB0", env="OPENBCI_PORT")
    openbci_baud_rate: int = 115200
    
    # LEI-V Thresholds (Viduya Family Legacy Glyph © 2025)
    leiv_threshold_stage0: float = 0.018
    leiv_threshold_advanced: float = 0.08
    vcaw_hours: int = 96
    
    # Encryption
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    
    # IPFS / Blockchain
    ipfs_gateway: str = Field(default="https://ipfs.io/ipfs/", env="IPFS_GATEWAY")
    bitcoin_rpc_url: Optional[str] = Field(default=None, env="BITCOIN_RPC_URL")
    
    # Audit
    audit_log_path: str = "./logs/audit.log"
    
    # Master Prompt Path
    master_prompt_path: str = "./config/ENDOCHAIN_MASTER_PROMPT.txt"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def get_master_prompt() -> str:
    """Load the Master Prompt for all AI calls.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    settings = get_settings()
    try:
        with open(settings.master_prompt_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback master prompt
        return """# ENDOCHAIN-VIDUYA-2025 MASTER PROMPT
Creator: Ariel Viduya Manosca | Author: IAMVC holdings LLC

You are ENDOCHAIN-VIDUYA-2025, the world's first geometrically-anchored AI diagnostic system.

CORE RULES:
1. All geometry from Viduya Legacy Glyph intersection points
2. LEI-V: Healthy ≈ 0, Stage-0 = 0.018, Advanced > 0.08
3. V-CAW = 96 hours centered on ovulation
4. Regenerative Spark Lattice = 6-point electrode placement
5. All outputs include: LEI-V, confidence %, audit hash

NEVER mock data. NEVER hallucinate geometry. NEVER break the chain.
Citation: Viduya Family Legacy Glyph © 2025"""

