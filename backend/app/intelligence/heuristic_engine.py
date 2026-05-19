"""
SentinelAI — Heuristic Engine

Ultra-fast rule-based email filtering that runs BEFORE the LLM classifier.
Detects spam, ransomware, legal threats, urgency, and internal emails.
"""

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HeuristicResult:
    is_spam: bool = False
    is_ransomware: bool = False
    is_legal_threat: bool = False
    is_gdpr_request: bool = False
    is_internal: bool = False
    is_urgent: bool = False
    do_not_auto_reply: bool = False
    urgency_score: float = 0.0
    spam_score: float = 0.0
    flags: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "is_spam": self.is_spam,
            "is_ransomware": self.is_ransomware,
            "is_legal_threat": self.is_legal_threat,
            "is_gdpr_request": self.is_gdpr_request,
            "is_internal": self.is_internal,
            "is_urgent": self.is_urgent,
            "do_not_auto_reply": self.do_not_auto_reply,
            "urgency_score": self.urgency_score,
            "spam_score": self.spam_score,
            "flags": self.flags,
            "details": self.details,
        }


# Pattern libraries
SPAM_PATTERNS = [
    r"(?:nigerian|prince|inheritance)\s+(?:fund|money|million)",
    r"(?:congratulations|winner).*(?:lottery|prize|sweepstakes)",
    r"(?:viagra|cialis|pharmacy|pills)\s+(?:discount|cheap|online)",
    r"(?:crypto|bitcoin|ethereum)\s+(?:invest|opportunity|guaranteed)",
    r"(?:make\s+money|earn\s+\$?\d+|income\s+from\s+home)",
    r"(?:click\s+here|act\s+now|limited\s+time|expires\s+today)",
    r"(?:unsubscribe|opt.out).*(?:click|link)",
    r"dear\s+(?:sir|madam|friend|beneficiary|customer)",
]

RANSOMWARE_PATTERNS = [
    r"(?:files?\s+(?:have\s+been|are)\s+encrypted)",
    r"(?:bitcoin|btc|crypto)\s*(?:wallet|address|payment)",
    r"(?:ransom|decrypt(?:ion)?)\s*(?:key|tool|software)",
    r"(?:pay|send|transfer)\s*(?:\$|usd|btc)?\s*\d+",
    r"(?:deadline|countdown|time\s+limit)\s*(?:expires?|hours?|days?)",
    r"(?:data\s+(?:will\s+be|has\s+been)\s+(?:leaked|published|deleted))",
    r"(?:we\s+have\s+(?:access|control)\s+(?:to|of)\s+your)",
]

LEGAL_PATTERNS = [
    r"(?:lawsuit|litigation|legal\s+action|court\s+order)",
    r"(?:attorney|lawyer|counsel|solicitor)\s+(?:representing|on\s+behalf)",
    r"(?:cease\s+and\s+desist|cease\s*&\s*desist)",
    r"(?:subpoena|summons|deposition|injunction)",
    r"(?:breach\s+of\s+(?:contract|agreement|terms))",
    r"(?:intellectual\s+property|copyright\s+infringement|trademark)",
    r"(?:we\s+(?:will|shall)\s+(?:pursue|seek)\s+(?:legal|damages))",
    r"(?:liability|negligence|malpractice)",
]

GDPR_PATTERNS = [
    r"(?:gdpr|data\s+protection\s+(?:act|regulation))",
    r"(?:right\s+to\s+(?:be\s+forgotten|erasure|deletion|access))",
    r"(?:data\s+subject\s+(?:access\s+)?request|dsar)",
    r"(?:personal\s+data|personally\s+identifiable)",
    r"(?:data\s+portability|data\s+breach\s+notification)",
]

URGENCY_PATTERNS = [
    (r"(?:asap|a\.s\.a\.p\.|immediately|right\s+away|urgent(?:ly)?)", 0.8),
    (r"(?:critical|emergency|crisis|outage|down)", 0.9),
    (r"(?:deadline|due\s+(?:date|today|tomorrow))", 0.7),
    (r"(?:escalat(?:e|ing|ion)|priority|time.sensitive)", 0.6),
    (r"(?:blocked|stuck|can'?t\s+proceed|showstopper)", 0.7),
]

INTERNAL_DOMAINS = [
    "sentinelai.com",
    "sentinel-ai.io",
    "internal.sentinel.com",
]


def _compile_patterns(patterns: list[str]) -> re.Pattern:
    return re.compile("|".join(patterns), re.IGNORECASE | re.MULTILINE)


_spam_re = _compile_patterns(SPAM_PATTERNS)
_ransomware_re = _compile_patterns(RANSOMWARE_PATTERNS)
_legal_re = _compile_patterns(LEGAL_PATTERNS)
_gdpr_re = _compile_patterns(GDPR_PATTERNS)
_urgency_compiled = [(re.compile(p, re.IGNORECASE), s) for p, s in URGENCY_PATTERNS]


def analyze_email(
    sender: str,
    subject: str,
    body: str,
    internal_domains: list[str] | None = None,
) -> HeuristicResult:
    """Run all heuristic checks on an email. Returns structured result."""
    result = HeuristicResult()
    full_text = f"{subject}\n{body}"
    domains = internal_domains or INTERNAL_DOMAINS

    # Internal check
    sender_domain = sender.split("@")[-1].lower() if "@" in sender else ""
    if sender_domain in [d.lower() for d in domains]:
        result.is_internal = True
        result.flags.append("internal_email")

    # Spam detection
    spam_matches = _spam_re.findall(full_text)
    if spam_matches:
        result.spam_score = min(len(spam_matches) * 0.3, 1.0)
        if result.spam_score >= 0.5:
            result.is_spam = True
            result.flags.append("spam_detected")
            result.details["spam_matches"] = spam_matches[:5]

    # Caps ratio boost for spam
    if len(body) > 20:
        caps_ratio = sum(1 for c in body if c.isupper()) / len(body)
        if caps_ratio > 0.5:
            result.spam_score = min(result.spam_score + 0.3, 1.0)
            result.flags.append("excessive_caps")

    # Ransomware detection
    ransom_matches = _ransomware_re.findall(full_text)
    if ransom_matches:
        result.is_ransomware = True
        result.do_not_auto_reply = True
        result.flags.append("ransomware_detected")
        result.details["ransomware_matches"] = ransom_matches[:5]

    # Legal threat detection
    legal_matches = _legal_re.findall(full_text)
    if legal_matches:
        result.is_legal_threat = True
        result.do_not_auto_reply = True
        result.flags.append("legal_threat")
        result.details["legal_matches"] = legal_matches[:5]

    # GDPR request detection
    gdpr_matches = _gdpr_re.findall(full_text)
    if gdpr_matches:
        result.is_gdpr_request = True
        result.do_not_auto_reply = True
        result.flags.append("gdpr_request")
        result.details["gdpr_matches"] = gdpr_matches[:3]

    # Urgency scoring
    max_urgency = 0.0
    for pattern, score in _urgency_compiled:
        if pattern.search(full_text):
            max_urgency = max(max_urgency, score)
            result.flags.append(f"urgency_{score}")

    # Exclamation density adds to urgency
    excl_count = full_text.count("!")
    if excl_count > 3:
        max_urgency = min(max_urgency + 0.1, 1.0)

    result.urgency_score = max_urgency
    result.is_urgent = max_urgency >= 0.7

    return result
