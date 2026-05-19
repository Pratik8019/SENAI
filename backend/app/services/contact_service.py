"""
SentinelAI — Contact Service
"""

import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Contact


async def get_contact(db: AsyncSession, contact_id: uuid.UUID) -> Contact | None:
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalar_one_or_none()


async def get_contact_by_email(db: AsyncSession, email: str) -> Contact | None:
    result = await db.execute(select(Contact).where(Contact.email == email))
    return result.scalar_one_or_none()


async def get_contact_profile(db: AsyncSession, contact_id: uuid.UUID) -> dict:
    """Build enriched contact profile for agent/LLM context."""
    contact = await get_contact(db, contact_id)
    if not contact:
        return {}
    return {
        "id": str(contact.id),
        "email": contact.email,
        "name": contact.name,
        "company": contact.company,
        "domain": contact.domain,
        "risk_score": contact.risk_score,
        "total_emails": contact.total_emails,
        "metadata": contact.metadata_ or {},
        "notes": contact.notes,
        "member_since": contact.created_at.isoformat(),
    }


async def get_contacts_paginated(
    db: AsyncSession, page: int = 1, page_size: int = 20
) -> tuple[list[Contact], int]:
    query = select(Contact).order_by(Contact.created_at.desc())
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total
