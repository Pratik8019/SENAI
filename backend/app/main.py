"""
SentinelAI Mission Control — FastAPI Application

Production-grade AI-powered CRM Intelligence Platform.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    app.state.debug = settings.debug
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=(
            "Production-grade AI-powered CRM Intelligence Platform. "
            "Ingests emails, performs heuristic filtering, uses RAG for grounded responses, "
            "and runs autonomous ReAct-style AI agents."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware (order matters: last added = first executed)
    from app.middleware.error_handler import ErrorHandlerMiddleware
    from app.middleware.sanitization import SanitizationMiddleware
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(SanitizationMiddleware)

    # Routes
    app.include_router(api_router)

    # Health check
    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "healthy", "service": "sentinel-api"}

    return app


app = create_app()
