"""
SentinelAI — Threat Detector

Detects legal, security, and compliance threats for escalation.
"""

from dataclasses import dataclass, field


@dataclass
class ThreatAssessment:
    threat_level: str = "none"  # none, low, medium, high, critical
    threat_types: list[str] = field(default_factory=list)
    requires_escalation: bool = False
    escalation_targets: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "threat_level": self.threat_level,
            "threat_types": self.threat_types,
            "requires_escalation": self.requires_escalation,
            "escalation_targets": self.escalation_targets,
            "details": self.details,
        }


def assess_threat(heuristic_flags: list[str], classification: dict | None = None) -> ThreatAssessment:
    """Combine heuristic flags with AI classification to assess threat level."""
    assessment = ThreatAssessment()
    score = 0

    if "ransomware_detected" in heuristic_flags:
        assessment.threat_types.append("ransomware")
        assessment.escalation_targets.extend(["security_team", "ciso"])
        score += 4

    if "legal_threat" in heuristic_flags:
        assessment.threat_types.append("legal")
        assessment.escalation_targets.append("legal_team")
        score += 3

    if "gdpr_request" in heuristic_flags:
        assessment.threat_types.append("compliance")
        assessment.escalation_targets.append("dpo")
        score += 2

    if classification:
        if classification.get("category") == "security":
            score += 2
            assessment.threat_types.append("security_concern")
        risk_indicators = classification.get("risk_indicators", [])
        for risk in risk_indicators:
            if risk == "data_breach":
                score += 3
                assessment.escalation_targets.append("security_team")
            elif risk == "churn_risk":
                score += 1
                assessment.escalation_targets.append("customer_success")

    # Determine level
    if score >= 4:
        assessment.threat_level = "critical"
    elif score >= 3:
        assessment.threat_level = "high"
    elif score >= 2:
        assessment.threat_level = "medium"
    elif score >= 1:
        assessment.threat_level = "low"

    assessment.requires_escalation = score >= 2
    assessment.escalation_targets = list(set(assessment.escalation_targets))

    return assessment
