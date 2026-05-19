"""
SentinelAI — Contact Model

Represents a customer/sender with enrichment data and risk scoring.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255))
    domain: Mapped[str | None] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(50))
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    total_emails: Mapped[int] = mapped_column(default=0)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, default=dict)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    threads = relationship("Thread", back_populates="contact", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Contact {self.email}>"
