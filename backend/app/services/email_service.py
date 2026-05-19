"""
SentinelAI — Email Service

Core business logic for email ingestion, deduplication, thread linking, and priority scoring.
"""

import re
import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Email, Thread, Contact, EmailDirection, ThreadPriority
from app.schemas.email import EmailIngestPayload
from app.core.security import hash_message_id, sanitize_input
from app.intelligence.heuristic_engine import analyze_email
from app.intelligence.sentiment import quick_sentiment_score


async def ingest_email(db: AsyncSession, payload: EmailIngestPayload) -> Email:
    """
    Full ingestion pipeline for a single email:
    1. Duplicate detection
    2. Contact resolution
    3. Thread linking
    4. Heuristic analysis
    5. Priority scoring
    """
    # 1. Duplicate detection via message_id hash
    msg_hash = hash_message_id(payload.message_id)
    existing = await db.execute(
        select(Email).where(Email.message_id_hash == msg_hash)
    )
    if existing.scalar_one_or_none():
        raise ValueError(f"Duplicate email: {payload.message_id}")

    # 2. Contact resolution — find or create
    contact = await _resolve_contact(db, payload.sender, payload.sender_name)

    # 3. Thread linking
    thread = await _resolve_thread(db, payload, contact)

    # 4. Heuristic analysis
    sanitized_body = sanitize_input(payload.body)
    sanitized_subject = sanitize_input(payload.subject)
    heuristic = analyze_email(payload.sender, sanitized_subject, sanitized_body)

    # 5. Sentiment pre-scoring
    sentiment_label, sentiment_score = quick_sentiment_score(sanitized_body)

    # 6. Priority scoring
    priority_score = _calculate_priority(heuristic, contact.risk_score, sentiment_score)

    # Create email record
    email = Email(
        id=uuid.uuid4(),
        thread_id=thread.id,
        message_id=payload.message_id,
        message_id_hash=msg_hash,
        in_reply_to=payload.in_reply_to,
        references=payload.references,
        sender=payload.sender,
        sender_name=payload.sender_name,
        recipients=payload.recipients,
        subject=payload.subject,
        body=payload.body,
        body_html=payload.body_html,
        direction=EmailDirection.INBOUND,
        headers=payload.headers or {},
        heuristic_result=heuristic.to_dict(),
        priority_score=priority_score,
        received_at=payload.received_at or datetime.now(timezone.utc),
        requires_human=heuristic.do_not_auto_reply,
    )

    db.add(email)

    # Update thread stats
    thread.email_count += 1
    thread.last_activity_at = datetime.now(timezone.utc)
    thread.sentiment_score = sentiment_score
    if thread.sentiment_trend is None:
        thread.sentiment_trend = []
    thread.sentiment_trend = thread.sentiment_trend + [
        {"score": sentiment_score, "label": sentiment_label, "ts": datetime.now(timezone.utc).isoformat()}
    ]

    # Update priority based on heuristic flags
    if heuristic.is_legal_threat or heuristic.is_ransomware:
        thread.priority = ThreadPriority.CRITICAL
    elif heuristic.is_urgent:
        thread.priority = ThreadPriority.HIGH

    # Update contact stats
    contact.total_emails += 1

    await db.flush()
    return email


async def _resolve_contact(db: AsyncSession, email_addr: str, name: str | None) -> Contact:
    """Find existing contact or create new one."""
    result = await db.execute(
        select(Contact).where(Contact.email == email_addr)
    )
    contact = result.scalar_one_or_none()

    if contact:
        if name and not contact.name:
            contact.name = name
        return contact

    domain = email_addr.split("@")[-1] if "@" in email_addr else None
    contact = Contact(
        id=uuid.uuid4(),
        email=email_addr,
        name=name,
        domain=domain,
    )
    db.add(contact)
    await db.flush()
    return contact


async def _resolve_thread(db: AsyncSession, payload: EmailIngestPayload, contact: Contact) -> Thread:
    """Link email to existing thread or create new one."""
    # Try to find by In-Reply-To header
    if payload.in_reply_to:
        ref_hash = hash_message_id(payload.in_reply_to)
        result = await db.execute(
            select(Email).where(Email.message_id_hash == ref_hash)
        )
        parent = result.scalar_one_or_none()
        if parent:
            result = await db.execute(
                select(Thread).where(Thread.id == parent.thread_id)
            )
            thread = result.scalar_one_or_none()
            if thread:
                return thread

    # Try subject matching (strip Re:, Fwd:, etc.)
    clean_subject = re.sub(r'^(?:Re|Fwd|Fw):\s*', '', payload.subject, flags=re.IGNORECASE).strip()
    if clean_subject:
        result = await db.execute(
            select(Thread).where(
                Thread.subject.ilike(f"%{clean_subject[:100]}%"),
                Thread.contact_id == contact.id,
            )
        )
        existing_thread = result.scalar_one_or_none()
        if existing_thread:
            return existing_thread

    # Create new thread
    thread = Thread(
        id=uuid.uuid4(),
        subject=payload.subject,
        contact_id=contact.id,
    )
    db.add(thread)
    await db.flush()
    return thread


def _calculate_priority(heuristic, contact_risk: float, sentiment_score: float) -> float:
    """Weighted priority formula: urgency×3 + sender_risk×2 + negativity×1."""
    urgency_component = heuristic.urgency_score * 3.0
    risk_component = min(contact_risk, 1.0) * 2.0
    sentiment_component = max(0, -sentiment_score) * 1.0

    # Bonus for critical flags
    if heuristic.is_ransomware:
        urgency_component += 3.0
    elif heuristic.is_legal_threat:
        urgency_component += 2.0

    score = urgency_component + risk_component + sentiment_component
    return round(min(score / 10.0, 1.0), 3)


async def get_emails_paginated(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    status_filter: str | None = None,
    urgency_filter: str | None = None,
) -> tuple[list[Email], int]:
    """Paginated email retrieval with optional filters."""
    query = select(Email).order_by(Email.received_at.desc())

    if status_filter == "needs_review":
        query = query.where(Email.requires_human == True)
    elif status_filter == "processed":
        query = query.where(Email.is_processed == True)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    emails = list(result.scalars().all())

    return emails, total
