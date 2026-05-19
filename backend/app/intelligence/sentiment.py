"""
SentinelAI — Sentiment Analysis

Rule-based + LLM sentiment scoring for email text.
"""

import re


# Quick lexicon for fast scoring without LLM
POSITIVE_WORDS = {
    "thank", "thanks", "appreciate", "great", "excellent", "wonderful", "happy",
    "pleased", "satisfied", "love", "amazing", "perfect", "fantastic", "helpful",
    "resolved", "fixed", "working", "impressed", "recommend", "best",
}

NEGATIVE_WORDS = {
    "angry", "frustrated", "disappointed", "terrible", "awful", "horrible",
    "unacceptable", "worst", "furious", "outraged", "disgusted", "useless",
    "broken", "failure", "incompetent", "ridiculous", "pathetic", "scam",
    "waste", "cancel", "lawsuit", "complaint", "refund",
}

THREATENING_WORDS = {
    "sue", "lawsuit", "attorney", "lawyer", "legal", "court", "report",
    "regulator", "bbb", "media", "public", "expose", "consequences",
}


def quick_sentiment_score(text: str) -> tuple[str, float]:
    """
    Fast lexicon-based sentiment scoring.
    Returns (sentiment_label, score) where score is -1.0 to 1.0.
    """
    words = set(re.findall(r'\b\w+\b', text.lower()))

    pos_count = len(words & POSITIVE_WORDS)
    neg_count = len(words & NEGATIVE_WORDS)
    threat_count = len(words & THREATENING_WORDS)

    total = pos_count + neg_count + threat_count
    if total == 0:
        return "neutral", 0.0

    score = (pos_count - neg_count - threat_count * 1.5) / (total + 1)
    score = max(-1.0, min(1.0, score))

    if threat_count > 0:
        label = "threatening"
    elif score > 0.3:
        label = "positive"
    elif score < -0.3:
        label = "negative"
    elif score < -0.6:
        label = "angry"
    else:
        label = "neutral"

    return label, round(score, 3)
