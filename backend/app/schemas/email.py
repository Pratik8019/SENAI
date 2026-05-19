"""
SentinelAI — Email Schemas

Pydantic models for email ingestion, responses, and classification.
"""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class EmailIngestPayload(BaseModel):
    """Schema for a single email in the ingestion endpoint."""
    message_id: str = Field(..., description="Unique email Message-ID header")
    in_reply_to: str | None = Field(None, description="Message-ID of parent email")
    references: str | None = Field(None, description="Space-separated Message-IDs of thread")
    sender: str = Field(..., description="Sender email address")
    sender_name: str | None = Field(None, description="Sender display name")
    recipients: list[str] = Field(default_factory=list, description="Recipient addresses")
    subject: str = Field(..., min_length=1, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body text")
    body_html: str | None = Field(None, description="HTML version of body")
    headers: dict | None = Field(default_factory=dict, description="Raw email headers")
    received_at: datetime | None = Field(None, description="When the email was received")


class EmailBatchIngest(BaseModel):
    """Batch email ingestion request."""
    emails: list[EmailIngestPayload] = Field(..., min_length=1, max_length=100)


class EmailResponse(BaseModel):
    """Standard email response."""
    id: UUID
    thread_id: UUID
    message_id: str
    sender: str
    sender_name: str | None
    subject: str
    body: str
    direction: str
    heuristic_result: dict | None
    classification: dict | None
    confidence_score: float | None
    priority_score: float | None
    is_processed: bool
    requires_human: bool
    received_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class EmailListResponse(BaseModel):
    """Paginated email list."""
    emails: list[EmailResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
