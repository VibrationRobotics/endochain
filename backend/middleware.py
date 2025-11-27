# ENDOCHAIN Backend: Middleware
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
"""
Custom middleware for audit logging and rate limiting.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from datetime import datetime
import hashlib
import json
import logging
import time
from typing import Callable

logger = logging.getLogger("endochain.middleware")


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware for comprehensive request/response audit logging.
    
    All API calls are logged with 256-bit hashes for regulatory compliance.
    FDA 21 CFR Part 11 compliant audit trail.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Extract request metadata
        request_id = request.headers.get("X-Request-ID", self._generate_request_id())
        client_ip = request.client.host if request.client else "unknown"
        
        # Process request
        response = await call_next(request)
        
        # Calculate timing
        process_time = time.time() - start_time
        
        # Generate audit hash
        audit_data = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": str(request.url.path),
            "client_ip": client_ip,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2)
        }
        audit_hash = hashlib.sha256(
            json.dumps(audit_data, sort_keys=True).encode()
        ).hexdigest()
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Audit-Hash"] = audit_hash
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        response.headers["X-Citation"] = "Viduya Family Legacy Glyph (C) 2025"
        
        # Log for audit trail
        logger.info(
            f"[AUDIT] {request.method} {request.url.path} "
            f"status={response.status_code} time={process_time:.4f}s "
            f"hash={audit_hash[:16]}..."
        )
        
        return response
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        import uuid
        return f"ENDO-{str(uuid.uuid4())[:8].upper()}"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for API protection."""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._request_counts: dict = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_minute = datetime.utcnow().strftime("%Y%m%d%H%M")
        key = f"{client_ip}:{current_minute}"
        
        # Check rate limit
        count = self._request_counts.get(key, 0)
        if count >= self.requests_per_minute:
            return Response(
                content=json.dumps({
                    "error": "Rate limit exceeded",
                    "retry_after_seconds": 60
                }),
                status_code=429,
                media_type="application/json"
            )
        
        # Increment counter
        self._request_counts[key] = count + 1
        
        # Cleanup old entries
        self._cleanup_old_entries(current_minute)
        
        return await call_next(request)
    
    def _cleanup_old_entries(self, current_minute: str):
        """Remove rate limit entries from previous minutes."""
        keys_to_remove = [
            k for k in self._request_counts.keys()
            if not k.endswith(current_minute)
        ]
        for k in keys_to_remove:
            del self._request_counts[k]

