"""
SentinelAI — Thread Model

Groups related emails into conversation threads with status tracking.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum


class ThreadStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    AWAITING_REPLY = "awaiting_reply"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class ThreadPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    contact_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False, index=True
    )
    status: Mapped[ThreadStatus] = mapped_column(
        SAEnum(ThreadStatus), default=ThreadStatus.OPEN
    )
    priority: Mapped[ThreadPriority] = mapped_column(
        SAEnum(ThreadPriority), default=ThreadPriority.MEDIUM
    )
    category: Mapped[str | None] = mapped_column(String(100))
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0)
    sentiment_trend: Mapped[dict | None] = mapped_column(JSONB, default=list)
    email_count: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    contact = relationship("Contact", back_populates="threads", lazy="selectin")
    emails = relationship(
        "Email", back_populates="thread", lazy="selectin",
        order_by="Email.received_at"
    )

    def __repr__(self) -> str:
        return f"<Thread {self.subject[:50]}>"
