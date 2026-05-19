"""
SentinelAI — Classification Service

LLM-based email classification using OpenAI structured output.
Falls back to heuristic-based classification when API key is not configured.
"""

import json
import time
from openai import AsyncOpenAI
from app.core.config import get_settings
from app.schemas.classification import ClassificationResult

settings = get_settings()

client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

SYSTEM_PROMPT = """You are SentinelAI, an expert email classification system for a CRM platform.

Analyze the email thread below along with any retrieved policy context.

Your job is to:
1. Classify the email category
2. Assess sentiment and urgency
3. Determine if human review is needed
4. Extract key entities
5. Generate a suggested reply if appropriate
6. Flag risk indicators

IMPORTANT RULES:
- Never suggest auto-replies for legal threats, ransomware, or GDPR requests
- Be conservative with confidence scores
- Always explain escalation reasons
- Extract amounts, dates, product names as entities

Respond ONLY with valid JSON matching the required schema."""


async def classify_email(
    thread_history: str,
    rag_context: str | None = None,
    sender_profile: dict | None = None,
    heuristic_result: dict | None = None,
) -> ClassificationResult:
    """
    Classify an email using OpenAI structured output.
    Falls back to heuristic-based classification if no API key.
    """
    if not client or not settings.openai_api_key:
        return _fallback_classification(thread_history, heuristic_result)

    user_message = _build_classification_prompt(
        thread_history, rag_context, sender_profile, heuristic_result
    )

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=1000,
        )

        result_json = json.loads(response.choices[0].message.content)
        return ClassificationResult(**result_json)

    except Exception as e:
        # Fallback on any error
        return _fallback_classification(thread_history, heuristic_result)


def _build_classification_prompt(
    thread_history: str,
    rag_context: str | None,
    sender_profile: dict | None,
    heuristic_result: dict | None,
) -> str:
    parts = [f"## Email Thread\n{thread_history}"]

    if rag_context:
        parts.append(f"## Relevant Policy Context\n{rag_context}")
    if sender_profile:
        parts.append(f"## Sender Profile\n{json.dumps(sender_profile, indent=2)}")
    if heuristic_result:
        parts.append(f"## Heuristic Pre-Analysis\n{json.dumps(heuristic_result, indent=2)}")

    parts.append(
        '## Required Output Schema\n'
        '{"category": "support|billing|legal|security|feature_request|complaint|spam|general", '
        '"sentiment": "positive|neutral|negative|angry|threatening", '
        '"sentiment_score": -1.0 to 1.0, '
        '"urgency": "low|medium|high|critical", '
        '"confidence": 0.0 to 1.0, '
        '"requires_human": true/false, '
        '"escalation_reason": "string or null", '
        '"suggested_reply": "string or null", '
        '"entities": {"names": [], "amounts": [], "dates": [], "products": []}, '
        '"summary": "one line summary", '
        '"risk_indicators": ["legal_threat", "data_breach", "compliance", "churn_risk"]}'
    )

    return "\n\n".join(parts)


def _fallback_classification(thread_history: str, heuristic_result: dict | None) -> ClassificationResult:
    """Heuristic-only classification when LLM is unavailable."""
    hr = heuristic_result or {}

    if hr.get("is_spam"):
        category, sentiment, urgency = "spam", "neutral", "low"
    elif hr.get("is_ransomware"):
        category, sentiment, urgency = "security", "threatening", "critical"
    elif hr.get("is_legal_threat"):
        category, sentiment, urgency = "legal", "threatening", "critical"
    elif hr.get("is_gdpr_request"):
        category, sentiment, urgency = "legal", "neutral", "high"
    elif hr.get("is_urgent"):
        category, sentiment, urgency = "support", "negative", "high"
    else:
        category, sentiment, urgency = "general", "neutral", "medium"

    return ClassificationResult(
        category=category,
        sentiment=sentiment,
        sentiment_score=0.0,
        urgency=urgency,
        confidence=0.5,
        requires_human=hr.get("do_not_auto_reply", False),
        escalation_reason="Heuristic-based classification — LLM unavailable" if hr.get("do_not_auto_reply") else None,
        suggested_reply=None,
        entities={},
        summary=f"Email classified as {category} via heuristic fallback",
        risk_indicators=[f for f in ["legal_threat", "ransomware_detected", "gdpr_request"] if hr.get(f"is_{f.split('_')[0]}", False)],
    )
