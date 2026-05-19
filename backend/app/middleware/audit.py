"""
SentinelAI — Audit Middleware

Logs all API requests to the audit_logs table.
"""

import uuid
from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import async_session_factory
from app.models import AuditLog


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Only audit API calls
        if not request.url.path.startswith("/api"):
            return response

        try:
            async with async_session_factory() as session:
                log = AuditLog(
                    id=uuid.uuid4(),
                    actor="api_user",
                    action=request.method,
                    resource_type=request.url.path,
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    details={"status_code": response.status_code},
                )
                session.add(log)
                await session.commit()
        except Exception:
            pass  # Never fail the request due to audit logging

        return response
