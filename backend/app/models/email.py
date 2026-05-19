"""
SentinelAI — Email Model

Individual email messages with classification results and heuristic analysis.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum


class EmailDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Email(Base):
    __tablename__ = "emails"
    __table_args__ = (
        Index("ix_emails_thread_received", "thread_id", "received_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    thread_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("threads.id"), nullable=False, index=True
    )
    message_id: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    message_id_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    in_reply_to: Mapped[str | None] = mapped_column(String(500))
    references: Mapped[str | None] = mapped_column(Text)
    sender: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    sender_name: Mapped[str | None] = mapped_column(String(255))
    recipients: Mapped[list | None] = mapped_column(JSONB, default=list)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Mapped[str | None] = mapped_column(Text)
    direction: Mapped[EmailDirection] = mapped_column(
        SAEnum(EmailDirection), default=EmailDirection.INBOUND
    )
    headers: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    # Intelligence results
    heuristic_result: Mapped[dict | None] = mapped_column(JSONB)
    classification: Mapped[dict | None] = mapped_column(JSONB)
    confidence_score: Mapped[float | None] = mapped_column()
    priority_score: Mapped[float | None] = mapped_column()

    # Status
    is_processed: Mapped[bool] = mapped_column(default=False)
    requires_human: Mapped[bool] = mapped_column(default=False)
    is_auto_replied: Mapped[bool] = mapped_column(default=False)

    # Timestamps
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    thread = relationship("Thread", back_populates="emails", lazy="selectin")
    actions = relationship("Action", back_populates="email", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Email {self.message_id}>"
