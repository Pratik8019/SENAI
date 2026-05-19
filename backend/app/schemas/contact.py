"""
SentinelAI — Contact Schemas
"""

from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ContactResponse(BaseModel):
    id: UUID
    email: str
    name: str | None
    company: str | None
    domain: str | None
    phone: str | None
    risk_score: float
    total_emails: int
    metadata_: dict | None = None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContactListResponse(BaseModel):
    contacts: list[ContactResponse]
    total: int
    page: int
    page_size: int
