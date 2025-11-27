# ENDOCHAIN: Universal AI Platform Caller
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Universal interface for all AI platform integrations.

Provides:
- Unified API for all platforms
- Master Prompt injection for all calls
- Response normalization
- Error handling and retry logic
- Audit logging
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from backend.config import get_settings, get_master_prompt
from core.audit import AuditHasher

logger = logging.getLogger("endochain.ai")


class Platform(Enum):
    """Supported AI platforms."""
    MED_GEMINI = "med_gemini"
    AIDOC = "aidoc"
    TEMPUS = "tempus"
    VIZ_AI = "viz_ai"
    OPENEVIDENCE = "openevidence"


@dataclass
class PlatformResponse:
    """Normalized response from any AI platform."""
    platform: Platform
    success: bool
    confidence: float
    result: Dict[str, Any]
    raw_response: Optional[Dict[str, Any]]
    latency_ms: int
    error: Optional[str]
    timestamp: datetime
    audit_hash: str


class UniversalAICaller:
    """Universal caller for all AI platforms.
    
    All calls include the ENDOCHAIN Master Prompt and are logged
    to the immutable audit trail.
    
    Citation: Viduya Family Legacy Glyph © 2025
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.master_prompt = get_master_prompt()
        self.hasher = AuditHasher()
        self._clients: Dict[Platform, Any] = {}
    
    async def call_platform(
        self,
        platform: Platform,
        payload: Dict[str, Any],
        timeout: int = 30
    ) -> PlatformResponse:
        """Call a specific AI platform.
        
        Args:
            platform: Target platform
            payload: Platform-specific payload
            timeout: Request timeout in seconds
            
        Returns:
            Normalized PlatformResponse
        """
        start_time = datetime.utcnow()
        
        try:
            # Inject master prompt
            enhanced_payload = self._inject_master_prompt(platform, payload)
            
            # Get endpoint and API key
            endpoint, api_key = self._get_platform_config(platform)
            
            # Make API call
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "X-ENDOCHAIN-Version": "1.0.0"
                }
                
                async with session.post(
                    endpoint,
                    json=enhanced_payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    latency = int((datetime.utcnow() - start_time).total_seconds() * 1000)
                    
                    if response.status == 200:
                        raw = await response.json()
                        normalized = self._normalize_response(platform, raw)
                        
                        return PlatformResponse(
                            platform=platform,
                            success=True,
                            confidence=normalized.get("confidence", 0.0),
                            result=normalized,
                            raw_response=raw,
                            latency_ms=latency,
                            error=None,
                            timestamp=datetime.utcnow(),
                            audit_hash=self.hasher.hash_computation({
                                "platform": platform.value,
                                "result": normalized
                            })
                        )
                    else:
                        return self._error_response(
                            platform, f"HTTP {response.status}", start_time
                        )
                        
        except asyncio.TimeoutError:
            return self._error_response(platform, "Timeout", start_time)
        except Exception as e:
            logger.error(f"Platform {platform.value} error: {e}")
            return self._error_response(platform, str(e), start_time)
    
    async def call_all_platforms(
        self,
        payload: Dict[str, Any],
        platforms: Optional[List[Platform]] = None
    ) -> List[PlatformResponse]:
        """Call multiple platforms concurrently.
        
        Args:
            payload: Common payload (adapted per platform)
            platforms: Platforms to call (default: all)
            
        Returns:
            List of responses from all platforms
        """
        if platforms is None:
            platforms = list(Platform)
        
        tasks = [self.call_platform(p, payload) for p in platforms]
        return await asyncio.gather(*tasks)
    
    def _inject_master_prompt(
        self,
        platform: Platform,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Inject Master Prompt into platform-specific payload."""
        enhanced = payload.copy()
        
        if platform == Platform.MED_GEMINI:
            # Gemini uses system_instruction
            enhanced["system_instruction"] = self.master_prompt
        elif platform in [Platform.AIDOC, Platform.TEMPUS, Platform.VIZ_AI]:
            # These use context field
            enhanced["endochain_context"] = self.master_prompt
        elif platform == Platform.OPENEVIDENCE:
            # OpenEvidence uses query context
            enhanced["context"] = self.master_prompt
        
        return enhanced
    
    def _get_platform_config(self, platform: Platform) -> tuple:
        """Get endpoint and API key for platform."""
        configs = {
            Platform.MED_GEMINI: (self.settings.gemini_endpoint, self.settings.gemini_api_key),
            Platform.AIDOC: (self.settings.aidoc_endpoint, self.settings.aidoc_api_key),
            Platform.TEMPUS: (self.settings.tempus_endpoint, self.settings.tempus_api_key),
            Platform.VIZ_AI: (self.settings.viz_ai_endpoint, self.settings.viz_ai_api_key),
            Platform.OPENEVIDENCE: (self.settings.openevidence_endpoint, self.settings.openevidence_api_key),
        }
        return configs.get(platform, ("", ""))
    
    def _normalize_response(self, platform: Platform, raw: Dict) -> Dict[str, Any]:
        """Normalize platform-specific response to common format."""
        # Platform-specific normalization logic
        return {
            "platform": platform.value,
            "confidence": raw.get("confidence", raw.get("score", 0.0)),
            "findings": raw.get("findings", raw.get("results", [])),
            "citation": "Viduya Family Legacy Glyph © 2025"
        }
    
    def _error_response(self, platform: Platform, error: str, start: datetime) -> PlatformResponse:
        """Create error response."""
        latency = int((datetime.utcnow() - start).total_seconds() * 1000)
        return PlatformResponse(
            platform=platform,
            success=False,
            confidence=0.0,
            result={},
            raw_response=None,
            latency_ms=latency,
            error=error,
            timestamp=datetime.utcnow(),
            audit_hash=self.hasher.hash_computation({"platform": platform.value, "error": error})
        )

