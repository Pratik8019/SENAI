"""
SentinelAI — ReAct Autonomous Agent

Implements the Think → Act → Observe loop with tool execution
and full reasoning trace capture.
"""

import json
import re
import time
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.agents.tools import TOOL_MAP, get_tools_description
from app.agents.prompts import get_react_system_prompt
from app.schemas.agent import AgentStep, AgentResult

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


async def run_agent(
    email_id: uuid.UUID,
    email_body: str,
    email_subject: str,
    sender: str,
    thread_id: uuid.UUID | None = None,
    contact_id: uuid.UUID | None = None,
    db: AsyncSession | None = None,
    max_steps: int = 7,
) -> AgentResult:
    """
    Execute the ReAct agent loop on an email.
    Returns full reasoning trace and recommended actions.
    """
    start_time = time.time()
    steps: list[AgentStep] = []
    tools_used: set[str] = set()

    system_prompt = get_react_system_prompt()
    user_message = (
        f"Analyze this email and determine the best course of action.\n\n"
        f"**From:** {sender}\n"
        f"**Subject:** {email_subject}\n"
        f"**Thread ID:** {thread_id or 'N/A'}\n"
        f"**Contact ID:** {contact_id or 'N/A'}\n\n"
        f"**Email Body:**\n{email_body}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    # If no OpenAI client, run mock agent
    if not client or not settings.openai_api_key:
        return await _mock_agent_run(email_id, email_body, sender, thread_id, contact_id, db)

    for step_num in range(1, max_steps + 1):
        try:
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=0.2,
                max_tokens=800,
            )

            assistant_msg = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_msg})

            # Parse the response
            step = _parse_agent_response(assistant_msg, step_num)
            steps.append(step)

            # Check for final answer
            if "Final Answer:" in assistant_msg:
                break

            # Execute tool if action specified
            if step.action and step.action in TOOL_MAP:
                tools_used.add(step.action)
                tool = TOOL_MAP[step.action]

                kwargs = step.action_input or {}
                if db:
                    kwargs["db"] = db

                observation = await tool.execute(**kwargs)
                step.observation = observation

                messages.append({
                    "role": "user",
                    "content": f"Observation: {observation}",
                })
            elif step.action:
                messages.append({
                    "role": "user",
                    "content": f"Observation: Tool '{step.action}' not found. Available tools: {', '.join(TOOL_MAP.keys())}",
                })

        except Exception as e:
            steps.append(AgentStep(
                step_number=step_num,
                thought=f"Error in agent step: {str(e)}",
                timestamp=datetime.now(timezone.utc),
            ))
            break

    execution_time = (time.time() - start_time) * 1000

    # Extract final answer from last step
    final_answer = ""
    for step in reversed(steps):
        if step.thought and "Final Answer:" in (step.thought or ""):
            final_answer = step.thought.split("Final Answer:")[-1].strip()
            break
    if not final_answer and steps:
        final_answer = steps[-1].thought or "Agent completed without final answer."

    return AgentResult(
        email_id=email_id,
        final_answer=final_answer,
        steps=steps,
        tools_used=list(tools_used),
        total_steps=len(steps),
        execution_time_ms=round(execution_time, 2),
        confidence=0.75,
    )


def _parse_agent_response(text: str, step_num: int) -> AgentStep:
    """Parse the Think/Act/Observe format from agent response."""
    thought = ""
    action = None
    action_input = None

    # Extract Thought
    thought_match = re.search(r"Thought:\s*(.+?)(?=\nAction:|$)", text, re.DOTALL)
    if thought_match:
        thought = thought_match.group(1).strip()

    # Extract Final Answer as thought if present
    final_match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)
    if final_match:
        thought = text.strip()

    # Extract Action
    action_match = re.search(r"Action:\s*(\w+)", text)
    if action_match:
        action = action_match.group(1).strip()

    # Extract Action Input
    input_match = re.search(r"Action Input:\s*({.+?})", text, re.DOTALL)
    if input_match:
        try:
            action_input = json.loads(input_match.group(1))
        except json.JSONDecodeError:
            action_input = {"raw": input_match.group(1)}

    return AgentStep(
        step_number=step_num,
        thought=thought or text.strip(),
        action=action,
        action_input=action_input,
        timestamp=datetime.now(timezone.utc),
    )


async def _mock_agent_run(
    email_id: uuid.UUID,
    email_body: str,
    sender: str,
    thread_id: uuid.UUID | None,
    contact_id: uuid.UUID | None,
    db: AsyncSession | None,
) -> AgentResult:
    """Mock agent execution for when OpenAI is not available."""
    start_time = time.time()
    steps = []
    tools_used = []

    # Step 1: Think
    steps.append(AgentStep(
        step_number=1,
        thought="I need to analyze this email. Let me first search the knowledge base for relevant policies.",
        action="search_knowledge_base",
        action_input={"query": email_body[:100]},
        timestamp=datetime.now(timezone.utc),
    ))

    # Execute KB search
    kb_tool = TOOL_MAP["search_knowledge_base"]
    obs1 = await kb_tool.execute(query=email_body[:100])
    steps[0].observation = obs1
    tools_used.append("search_knowledge_base")

    # Step 2: Check account
    steps.append(AgentStep(
        step_number=2,
        thought="Let me check the sender's account status to understand their context.",
        action="check_account_status",
        action_input={"email": sender},
        timestamp=datetime.now(timezone.utc),
    ))
    acct_tool = TOOL_MAP["check_account_status"]
    obs2 = await acct_tool.execute(email=sender)
    steps[1].observation = obs2
    tools_used.append("check_account_status")

    # Step 3: Draft reply
    steps.append(AgentStep(
        step_number=3,
        thought="Based on my analysis, I'll draft a professional reply addressing the customer's concerns.",
        action="draft_reply",
        action_input={"context": email_body[:200], "tone": "professional"},
        timestamp=datetime.now(timezone.utc),
    ))
    draft_tool = TOOL_MAP["draft_reply"]
    obs3 = await draft_tool.execute(context=email_body[:200], tone="professional")
    steps[2].observation = obs3
    tools_used.append("draft_reply")

    # Step 4: Final answer
    steps.append(AgentStep(
        step_number=4,
        thought=(
            "Final Answer: Based on my analysis, this email requires standard support handling. "
            "I've reviewed the relevant policies, checked the customer's account status, and drafted a reply. "
            "Recommended actions: 1) Send the drafted reply, 2) Monitor for follow-up. "
            "Confidence: 0.72"
        ),
        timestamp=datetime.now(timezone.utc),
    ))

    execution_time = (time.time() - start_time) * 1000

    return AgentResult(
        email_id=email_id,
        final_answer=(
            "Based on my analysis, this email requires standard support handling. "
            "I've reviewed the relevant policies, checked the customer's account status, and drafted a reply. "
            "Recommended actions: 1) Send the drafted reply, 2) Monitor for follow-up."
        ),
        steps=steps,
        tools_used=tools_used,
        total_steps=len(steps),
        execution_time_ms=round(execution_time, 2),
        suggested_actions=["send_draft_reply", "monitor_thread"],
        confidence=0.72,
    )
