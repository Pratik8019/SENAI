"""
SentinelAI — Analytics Schemas
"""

from pydantic import BaseModel
from datetime import datetime


class SentimentTrendPoint(BaseModel):
    date: str
    score: float
    count: int


class CategoryCount(BaseModel):
    category: str
    count: int
    percentage: float


class EscalationHeatmapCell(BaseModel):
    day: int
    hour: int
    count: int


class AIPerformanceMetrics(BaseModel):
    total_processed: int
    auto_resolved: int
    auto_resolve_rate: float
    avg_confidence: float
    avg_processing_time_ms: float
    requires_human_count: int
    escalation_count: int


class AtRiskCustomer(BaseModel):
    contact_id: str
    email: str
    name: str | None
    company: str | None
    risk_score: float
    recent_sentiment: float
    total_threads: int
    last_activity: datetime


class AnalyticsDashboard(BaseModel):
    sentiment_trend: list[SentimentTrendPoint]
    categories: list[CategoryCount]
    escalation_heatmap: list[EscalationHeatmapCell]
    ai_performance: AIPerformanceMetrics
    at_risk_customers: list[AtRiskCustomer]
    total_emails: int
    total_threads: int
    total_contacts: int
