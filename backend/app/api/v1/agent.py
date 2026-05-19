"""
SentinelAI — Agent Endpoints
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.schemas.agent import AgentDryRunRequest, AgentDryRunResponse
from app.agents.react_agent import run_agent
from app.models import Email

router = APIRouter(tags=["Agent"])


@router.post("/agent/dry-run/{email_id}", response_model=AgentDryRunResponse)
async def agent_dry_run(
    email_id: uuid.UUID,
    request: AgentDryRunRequest | None = None,
    db: AsyncSession = Depends(get_database),
):
    """
    Run the ReAct AI agent on an email without taking real actions.
    Returns full reasoning trace and suggested actions.
    """
    # Fetch email
    result = await db.execute(select(Email).where(Email.id == email_id))
    email = result.scalar_one_or_none()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    try:
        agent_result = await run_agent(
            email_id=email.id,
            email_body=email.body,
            email_subject=email.subject,
            sender=email.sender,
            thread_id=email.thread_id,
            contact_id=None,
            db=db,
            max_steps=request.max_steps if request else 7,
        )

        return AgentDryRunResponse(success=True, result=agent_result)

    except Exception as e:
        return AgentDryRunResponse(success=False, result=None, error=str(e))
