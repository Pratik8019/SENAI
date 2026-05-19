"""
SentinelAI — Notification Service

Escalation notifications and internal alerting.
"""

import structlog
from app.intelligence.threat_detector import ThreatAssessment

logger = structlog.get_logger()


async def notify_escalation(
    email_id: str,
    thread_id: str,
    assessment: ThreatAssessment,
) -> None:
    """Send escalation notifications to appropriate teams."""
    for target in assessment.escalation_targets:
        logger.warning(
            "escalation_triggered",
            email_id=email_id,
            thread_id=thread_id,
            threat_level=assessment.threat_level,
            target=target,
            threat_types=assessment.threat_types,
        )
    # In production, this would send Slack/email/PagerDuty notifications
