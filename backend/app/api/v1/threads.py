"""
SentinelAI — Thread Endpoints
"""

import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.schemas.thread import ThreadListResponse, ThreadDetailResponse, ThreadResponse, ContactBrief
from app.schemas.email import EmailResponse
from app.services.thread_service import get_threads_paginated, get_thread_detail

router = APIRouter(tags=["Threads"])


@router.get("/threads", response_model=ThreadListResponse)
async def list_threads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    priority: str | None = None,
    db: AsyncSession = Depends(get_database),
):
    threads, total = await get_threads_paginated(db, page, page_size, status, priority)
    return ThreadListResponse(
        threads=[ThreadResponse.model_validate(t) for t in threads],
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total,
    )


@router.get("/threads/{thread_id}", response_model=ThreadDetailResponse)
async def get_thread(
    thread_id: uuid.UUID,
    db: AsyncSession = Depends(get_database),
):
    thread = await get_thread_detail(db, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return ThreadDetailResponse(
        id=thread.id,
        subject=thread.subject,
        contact_id=thread.contact_id,
        status=thread.status.value if hasattr(thread.status, 'value') else thread.status,
        priority=thread.priority.value if hasattr(thread.priority, 'value') else thread.priority,
        category=thread.category,
        sentiment_score=thread.sentiment_score,
        sentiment_trend=thread.sentiment_trend,
        email_count=thread.email_count,
        last_activity_at=thread.last_activity_at,
        created_at=thread.created_at,
        emails=[EmailResponse.model_validate(e) for e in (thread.emails or [])],
        contact=ContactBrief.model_validate(thread.contact) if thread.contact else None,
    )
