"""
SentinelAI — Analytics Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database
from app.schemas.analytics import (
    AnalyticsDashboard, SentimentTrendPoint, CategoryCount,
    EscalationHeatmapCell, AIPerformanceMetrics, AtRiskCustomer,
)
from app.models import Email, Thread, Contact, Action, ActionType
from datetime import datetime, timezone, timedelta

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/dashboard", response_model=AnalyticsDashboard)
async def get_dashboard_analytics(
    db: AsyncSession = Depends(get_database),
):
    """Get comprehensive analytics for the dashboard."""

    # Total counts
    total_emails = (await db.execute(select(func.count(Email.id)))).scalar() or 0
    total_threads = (await db.execute(select(func.count(Thread.id)))).scalar() or 0
    total_contacts = (await db.execute(select(func.count(Contact.id)))).scalar() or 0

    # Sentiment trend (last 30 days, grouped by day)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    sentiment_trend = await _get_sentiment_trend(db, thirty_days_ago)

    # Category breakdown
    categories = await _get_category_counts(db)

    # Escalation heatmap
    heatmap = await _get_escalation_heatmap(db)

    # AI performance
    ai_perf = await _get_ai_performance(db, total_emails)

    # At-risk customers
    at_risk = await _get_at_risk_customers(db)

    return AnalyticsDashboard(
        sentiment_trend=sentiment_trend,
        categories=categories,
        escalation_heatmap=heatmap,
        ai_performance=ai_perf,
        at_risk_customers=at_risk,
        total_emails=total_emails,
        total_threads=total_threads,
        total_contacts=total_contacts,
    )


async def _get_sentiment_trend(db: AsyncSession, since: datetime) -> list[SentimentTrendPoint]:
    """Aggregate sentiment scores by day."""
    result = await db.execute(
        select(
            func.date_trunc("day", Email.received_at).label("day"),
            func.avg(Thread.sentiment_score).label("avg_score"),
            func.count(Email.id).label("count"),
        )
        .join(Thread, Email.thread_id == Thread.id)
        .where(Email.received_at >= since)
        .group_by("day")
        .order_by("day")
    )

    return [
        SentimentTrendPoint(
            date=row.day.strftime("%Y-%m-%d") if row.day else "",
            score=round(float(row.avg_score or 0), 3),
            count=int(row.count),
        )
        for row in result.all()
    ]


async def _get_category_counts(db: AsyncSession) -> list[CategoryCount]:
    result = await db.execute(
        select(Thread.category, func.count(Thread.id).label("count"))
        .where(Thread.category.isnot(None))
        .group_by(Thread.category)
    )

    rows = result.all()
    total = sum(r.count for r in rows) or 1

    return [
        CategoryCount(
            category=r.category or "uncategorized",
            count=r.count,
            percentage=round(r.count / total * 100, 1),
        )
        for r in rows
    ]


async def _get_escalation_heatmap(db: AsyncSession) -> list[EscalationHeatmapCell]:
    result = await db.execute(
        select(
            extract("dow", Action.created_at).label("day"),
            extract("hour", Action.created_at).label("hour"),
            func.count(Action.id).label("count"),
        )
        .where(Action.action_type == ActionType.ESCALATE)
        .group_by("day", "hour")
    )

    return [
        EscalationHeatmapCell(day=int(r.day), hour=int(r.hour), count=r.count)
        for r in result.all()
    ]


async def _get_ai_performance(db: AsyncSession, total_emails: int) -> AIPerformanceMetrics:
    processed = (await db.execute(
        select(func.count(Email.id)).where(Email.is_processed == True)
    )).scalar() or 0

    auto_resolved = (await db.execute(
        select(func.count(Email.id)).where(Email.is_auto_replied == True)
    )).scalar() or 0

    avg_conf = (await db.execute(
        select(func.avg(Email.confidence_score)).where(Email.confidence_score.isnot(None))
    )).scalar() or 0.0

    needs_human = (await db.execute(
        select(func.count(Email.id)).where(Email.requires_human == True)
    )).scalar() or 0

    escalations = (await db.execute(
        select(func.count(Action.id)).where(Action.action_type == ActionType.ESCALATE)
    )).scalar() or 0

    return AIPerformanceMetrics(
        total_processed=processed,
        auto_resolved=auto_resolved,
        auto_resolve_rate=round(auto_resolved / max(processed, 1) * 100, 1),
        avg_confidence=round(float(avg_conf), 3),
        avg_processing_time_ms=0,
        requires_human_count=needs_human,
        escalation_count=escalations,
    )


async def _get_at_risk_customers(db: AsyncSession) -> list[AtRiskCustomer]:
    result = await db.execute(
        select(Contact)
        .where(Contact.risk_score > 0.5)
        .order_by(Contact.risk_score.desc())
        .limit(10)
    )

    contacts = result.scalars().all()
    return [
        AtRiskCustomer(
            contact_id=str(c.id),
            email=c.email,
            name=c.name,
            company=c.company,
            risk_score=c.risk_score,
            recent_sentiment=0.0,
            total_threads=0,
            last_activity=c.updated_at,
        )
        for c in contacts
    ]
