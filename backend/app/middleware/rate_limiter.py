"""
SentinelAI — Rate Limiter Middleware

Redis-backed sliding window rate limiting.
"""

import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import get_settings

settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        key = f"ratelimit:{client_ip}"

        try:
            from app.core.redis import redis_client
            current = await redis_client.get(key)
            if current and int(current) >= settings.rate_limit_per_minute:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please retry after 60 seconds.",
                )
            pipe = redis_client.pipeline()
            await pipe.incr(key)
            await pipe.expire(key, 60)
            await pipe.execute()
        except HTTPException:
            raise
        except Exception:
            # If Redis is unavailable, allow the request
            pass

        response = await call_next(request)
        return response
