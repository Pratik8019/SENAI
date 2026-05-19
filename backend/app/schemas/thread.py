"""
SentinelAI — Thread Schemas
"""

from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from app.schemas.email import EmailResponse


class ThreadResponse(BaseModel):
    id: UUID
    subject: str
    contact_id: UUID
    status: str
    priority: str
    category: str | None
    sentiment_score: float
    sentiment_trend: list | None
    email_count: int
    last_activity_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ThreadDetailResponse(ThreadResponse):
    emails: list[EmailResponse] = []
    contact: "ContactBrief | None" = None


class ContactBrief(BaseModel):
    id: UUID
    email: str
    name: str | None
    company: str | None
    risk_score: float

    class Config:
        from_attributes = True


class ThreadListResponse(BaseModel):
    threads: list[ThreadResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


# Update forward refs
ThreadDetailResponse.model_rebuild()
