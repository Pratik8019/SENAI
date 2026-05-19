"""
SentinelAI — Thread Service

Thread management, context retrieval, and status operations.
"""

import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Thread, Email, Contact


async def get_thread_detail(db: AsyncSession, thread_id: uuid.UUID) -> Thread | None:
    """Get thread with all emails and contact info."""
    result = await db.execute(
        select(Thread)
        .options(selectinload(Thread.emails), selectinload(Thread.contact))
        .where(Thread.id == thread_id)
    )
    return result.scalar_one_or_none()


async def get_thread_history_text(db: AsyncSession, thread_id: uuid.UUID) -> str:
    """Get formatted thread history for LLM context."""
    result = await db.execute(
        select(Email)
        .where(Email.thread_id == thread_id)
        .order_by(Email.received_at.asc())
    )
    emails = result.scalars().all()

    history_parts = []
    for email in emails:
        history_parts.append(
            f"[{email.received_at.isoformat()}] From: {email.sender}\n"
            f"Subject: {email.subject}\n"
            f"---\n{email.body}\n"
        )
    return "\n---EMAIL SEPARATOR---\n".join(history_parts)


async def get_threads_paginated(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    priority: str | None = None,
) -> tuple[list[Thread], int]:
    """Paginated thread list with filters."""
    query = select(Thread).order_by(Thread.last_activity_at.desc())

    if status:
        query = query.where(Thread.status == status)
    if priority:
        query = query.where(Thread.priority == priority)

    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)

    return list(result.scalars().all()), total


async def update_thread_status(db: AsyncSession, thread_id: uuid.UUID, status: str) -> Thread | None:
    result = await db.execute(select(Thread).where(Thread.id == thread_id))
    thread = result.scalar_one_or_none()
    if thread:
        thread.status = status
        await db.flush()
    return thread
