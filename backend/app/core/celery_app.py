"""
SentinelAI — Celery Application

Async task queue for background processing of email classification,
agent workflows, and web intelligence scraping.
"""

from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "sentinel",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_routes={
        "app.services.email_service.process_email_task": {"queue": "emails"},
        "app.agents.react_agent.run_agent_task": {"queue": "agents"},
        "app.services.web_intelligence.scrape_task": {"queue": "scraping"},
    },
)

celery_app.autodiscover_tasks(["app.services", "app.agents"])
