"""
SentinelAI — Root API Router

Aggregates all v1 endpoint routers.
"""

from fastapi import APIRouter
from app.api.v1 import ingest, emails, threads, contacts, rag, agent, analytics, websocket

api_router = APIRouter()

# V1 endpoints
api_router.include_router(ingest.router, prefix="/api/v1")
api_router.include_router(emails.router, prefix="/api/v1")
api_router.include_router(threads.router, prefix="/api/v1")
api_router.include_router(contacts.router, prefix="/api/v1")
api_router.include_router(rag.router, prefix="/api/v1")
api_router.include_router(agent.router, prefix="/api/v1")
api_router.include_router(analytics.router, prefix="/api/v1")

# WebSocket (no prefix)
api_router.include_router(websocket.router)
