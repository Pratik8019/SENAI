"""
SentinelAI — Classification Schemas

Structured output schema for LLM classification results.
"""

from pydantic import BaseModel, Field


class ClassificationResult(BaseModel):
    """The AI classification output for an email."""
    category: str = Field(
        ...,
        description="Email category: support, billing, legal, security, feature_request, complaint, spam, general"
    )
    sentiment: str = Field(
        ..., description="Overall sentiment: positive, neutral, negative, angry, threatening"
    )
    sentiment_score: float = Field(
        ..., ge=-1.0, le=1.0, description="Sentiment score from -1.0 (very negative) to 1.0 (very positive)"
    )
    urgency: str = Field(
        ..., description="Urgency level: low, medium, high, critical"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="AI confidence in this classification"
    )
    requires_human: bool = Field(
        ..., description="Whether this email requires human review"
    )
    escalation_reason: str | None = Field(
        None, description="Reason for escalation if requires_human is true"
    )
    suggested_reply: str | None = Field(
        None, description="AI-generated suggested reply"
    )
    entities: dict = Field(
        default_factory=dict,
        description="Extracted entities: names, companies, amounts, dates, product references"
    )
    summary: str = Field(
        ..., description="One-line summary of the email content"
    )
    risk_indicators: list[str] = Field(
        default_factory=list,
        description="Detected risk flags: legal_threat, data_breach, compliance, churn_risk"
    )
