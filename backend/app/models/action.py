"""
SentinelAI — Action Model

Tracks all actions taken on emails: agent traces, escalations, replies, tickets.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum


class ActionType(str, enum.Enum):
    AGENT_RUN = "agent_run"
    AUTO_REPLY = "auto_reply"
    DRAFT_REPLY = "draft_reply"
    ESCALATE = "escalate"
    FLAG_LEGAL = "flag_legal"
    CREATE_TICKET = "create_ticket"
    CLASSIFY = "classify"
    HUMAN_REVIEW = "human_review"


class ActionStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, index=True
    )
    action_type: Mapped[ActionType] = mapped_column(
        SAEnum(ActionType), nullable=False
    )
    status: Mapped[ActionStatus] = mapped_column(
        SAEnum(ActionStatus), default=ActionStatus.PENDING
    )
    payload: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    result: Mapped[dict | None] = mapped_column(JSONB)
    agent_trace: Mapped[list | None] = mapped_column(JSONB)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    email = relationship("Email", back_populates="actions", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Action {self.action_type} for {self.email_id}>"
