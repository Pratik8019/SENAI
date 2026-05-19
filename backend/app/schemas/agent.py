"""
SentinelAI — Agent Schemas

ReAct agent input/output schemas and reasoning trace format.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class AgentStep(BaseModel):
    """A single Think→Act→Observe step in the agent trace."""
    step_number: int
    thought: str = Field(..., description="Agent's reasoning")
    action: str | None = Field(None, description="Tool chosen")
    action_input: dict | None = Field(None, description="Tool input parameters")
    observation: str | None = Field(None, description="Tool output / result")
    timestamp: datetime | None = None


class AgentResult(BaseModel):
    """Complete agent execution result."""
    email_id: UUID
    final_answer: str
    steps: list[AgentStep]
    tools_used: list[str]
    total_steps: int
    execution_time_ms: float
    suggested_actions: list[str] = []
    confidence: float = 0.0


class AgentDryRunRequest(BaseModel):
    """Request body for agent dry-run."""
    max_steps: int = Field(default=7, ge=1, le=15)
    include_rag: bool = True
    verbose: bool = False


class AgentDryRunResponse(BaseModel):
    """Response for agent dry-run endpoint."""
    success: bool
    result: AgentResult | None
    error: str | None = None
