"""
SentinelAI — Email Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.schemas.email import EmailListResponse, EmailResponse
from app.services.email_service import get_emails_paginated

router = APIRouter(tags=["Emails"])


@router.get("/emails", response_model=EmailListResponse)
async def list_emails(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    db: AsyncSession = Depends(get_database),
):
    emails, total = await get_emails_paginated(db, page, page_size, status)
    return EmailListResponse(
        emails=[EmailResponse.model_validate(e) for e in emails],
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total,
    )
