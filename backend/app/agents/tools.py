"""
SentinelAI — Agent Tool Definitions

Tools available to the ReAct autonomous agent.
Each tool has a name, description, and async execute function.
"""

import uuid
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.rag.pipeline import rag_search
from app.services.thread_service import get_thread_history_text, get_thread_detail
from app.services.contact_service import get_contact_profile


class Tool:
    def __init__(self, name: str, description: str, execute_fn):
        self.name = name
        self.description = description
        self.execute_fn = execute_fn

    async def execute(self, **kwargs) -> str:
        return await self.execute_fn(**kwargs)


async def _search_knowledge_base(query: str, **kwargs) -> str:
    result = await rag_search(query, top_k=3)
    if not result["results"]:
        return "No relevant knowledge base documents found."
    parts = []
    for r in result["results"]:
        parts.append(f"[{r['source_file']}] (relevance: {r['relevance_score']})\n{r['content'][:500]}")
    return "\n---\n".join(parts)


async def _get_thread_history(thread_id: str, db: AsyncSession = None, **kwargs) -> str:
    if db is None:
        return "Database session not available."
    try:
        tid = uuid.UUID(thread_id)
        history = await get_thread_history_text(db, tid)
        return history if history else "No thread history found."
    except Exception as e:
        return f"Error retrieving thread: {str(e)}"


async def _get_contact_profile_tool(contact_id: str, db: AsyncSession = None, **kwargs) -> str:
    if db is None:
        return "Database session not available."
    try:
        cid = uuid.UUID(contact_id)
        profile = await get_contact_profile(db, cid)
        if not profile:
            return "Contact not found."
        import json
        return json.dumps(profile, indent=2, default=str)
    except Exception as e:
        return f"Error: {str(e)}"


async def _check_account_status(email: str, **kwargs) -> str:
    """Simulated account status check."""
    return (
        f"Account for {email}:\n"
        f"  Status: Active\n"
        f"  Plan: Professional\n"
        f"  MRR: $149/seat × 12 seats = $1,788/month\n"
        f"  Contract: Annual, renews in 3 months\n"
        f"  Payment: Up to date\n"
        f"  Open tickets: 2\n"
        f"  Health score: 72/100"
    )


async def _draft_reply(context: str, tone: str = "professional", **kwargs) -> str:
    """Generate a draft reply based on context."""
    return (
        f"[DRAFT REPLY — Tone: {tone}]\n\n"
        f"Dear Customer,\n\n"
        f"Thank you for reaching out to us. Based on your message, I'd like to address your concerns.\n\n"
        f"Context considered: {context[:200]}...\n\n"
        f"We take this matter seriously and will ensure it's resolved promptly. "
        f"A member of our team will follow up within 24 hours with a detailed response.\n\n"
        f"Best regards,\nSentinelAI Support"
    )


async def _escalate_to_human(reason: str, priority: str = "high", **kwargs) -> str:
    return f"✅ Escalated to human review.\nReason: {reason}\nPriority: {priority}\nAssigned to: Support Team Lead"


async def _create_internal_ticket(
    title: str, description: str, priority: str = "medium", **kwargs
) -> str:
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    return f"✅ Internal ticket created.\nID: {ticket_id}\nTitle: {title}\nPriority: {priority}"


async def _flag_for_legal(reason: str, **kwargs) -> str:
    return f"🚨 LEGAL FLAG SET.\nReason: {reason}\nNotified: Legal Team, CISO\nAuto-reply: DISABLED"


async def _scrape_public_sentiment(company: str, **kwargs) -> str:
    """Simulated public sentiment scraping."""
    return (
        f"Public sentiment summary for '{company}':\n"
        f"  Trustpilot: 3.8/5 (234 reviews)\n"
        f"  G2: 4.2/5 (89 reviews)\n"
        f"  Twitter sentiment: Mostly neutral, some complaints about pricing\n"
        f"  Recent trends: Competitor X launched similar feature last week"
    )


# Tool registry
TOOLS = [
    Tool("search_knowledge_base", "Search internal knowledge base for policy/procedure information. Input: query (string)", _search_knowledge_base),
    Tool("get_thread_history", "Get full email thread conversation history. Input: thread_id (UUID string)", _get_thread_history),
    Tool("get_contact_profile", "Get enriched customer profile. Input: contact_id (UUID string)", _get_contact_profile_tool),
    Tool("check_account_status", "Check customer account status, plan, billing. Input: email (string)", _check_account_status),
    Tool("draft_reply", "Generate a draft email reply. Input: context (string), tone (string, optional)", _draft_reply),
    Tool("escalate_to_human", "Escalate to human agent for review. Input: reason (string), priority (string)", _escalate_to_human),
    Tool("create_internal_ticket", "Create an internal support ticket. Input: title (string), description (string), priority (string)", _create_internal_ticket),
    Tool("flag_for_legal", "Flag email for legal team review — disables auto-reply. Input: reason (string)", _flag_for_legal),
    Tool("scrape_public_sentiment", "Get public sentiment data for a company. Input: company (string)", _scrape_public_sentiment),
]

TOOL_MAP = {t.name: t for t in TOOLS}


def get_tools_description() -> str:
    """Format tool descriptions for the agent system prompt."""
    lines = []
    for t in TOOLS:
        lines.append(f"- **{t.name}**: {t.description}")
    return "\n".join(lines)
