"""
SentinelAI — Heuristic Engine Tests
"""

from app.intelligence.heuristic_engine import analyze_email


def test_normal_email():
    result = analyze_email(
        "customer@example.com",
        "Help with account",
        "Hi, I need help resetting my password. Thanks!"
    )
    assert not result.is_spam
    assert not result.is_ransomware
    assert not result.is_legal_threat
    assert not result.do_not_auto_reply


def test_spam_detection():
    result = analyze_email(
        "prince@nigeria.com",
        "You are the winner!",
        "Congratulations! You have won the lottery prize of $10 million. Click here to claim."
    )
    assert result.is_spam
    assert result.spam_score >= 0.5


def test_ransomware_detection():
    result = analyze_email(
        "hacker@dark.net",
        "Your files have been encrypted",
        "All your files have been encrypted. Send 5 BTC to bitcoin wallet bc1q123. You have 72 hours deadline."
    )
    assert result.is_ransomware
    assert result.do_not_auto_reply


def test_legal_threat_detection():
    result = analyze_email(
        "attorney@lawfirm.com",
        "Cease and Desist",
        "Our attorney representing XYZ Corp demands you cease and desist. We will pursue legal action and file a lawsuit."
    )
    assert result.is_legal_threat
    assert result.do_not_auto_reply


def test_gdpr_detection():
    result = analyze_email(
        "user@eu.com",
        "GDPR Data Request",
        "Under GDPR, I exercise my right to erasure. Please delete all my personal data."
    )
    assert result.is_gdpr_request
    assert result.do_not_auto_reply


def test_urgency_detection():
    result = analyze_email(
        "user@company.com",
        "URGENT: Production down",
        "Critical emergency! Our production system is down and we need help immediately. ASAP!"
    )
    assert result.is_urgent
    assert result.urgency_score >= 0.7


def test_internal_email():
    result = analyze_email(
        "employee@sentinelai.com",
        "Team meeting tomorrow",
        "Hey team, reminder about the standup meeting tomorrow at 10 AM."
    )
    assert result.is_internal
