"""
SentinelAI — Input Sanitization Middleware
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import detect_injection
import structlog

logger = structlog.get_logger()


class SanitizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check query params for injection attempts
        for key, value in request.query_params.items():
            if detect_injection(value):
                logger.warning("prompt_injection_detected", param=key, path=request.url.path)

        return await call_next(request)
