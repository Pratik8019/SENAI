"""
SentinelAI — Error Handler Middleware

Standardized error responses across the API.
"""

import traceback
import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(
                "unhandled_exception",
                path=request.url.path,
                method=request.method,
                error=str(e),
                traceback=traceback.format_exc(),
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_server_error",
                    "message": "An unexpected error occurred.",
                    "detail": str(e) if request.app.state.debug else None,
                },
            )
