"""SentinelAI — Models Package"""

from app.models.contact import Contact
from app.models.thread import Thread, ThreadStatus, ThreadPriority
from app.models.email import Email, EmailDirection
from app.models.action import Action, ActionType, ActionStatus
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.web_cache import WebIntelligenceCache
from app.models.audit_log import AuditLog

__all__ = [
    "Contact",
    "Thread", "ThreadStatus", "ThreadPriority",
    "Email", "EmailDirection",
    "Action", "ActionType", "ActionStatus",
    "KnowledgeChunk",
    "WebIntelligenceCache",
    "AuditLog",
]
