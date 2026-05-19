"""SentinelAI — Test Configuration"""

import pytest


@pytest.fixture
def sample_email_payload():
    return {
        "message_id": "<test-001@example.com>",
        "sender": "customer@example.com",
        "sender_name": "Test Customer",
        "recipients": ["support@sentinelai.com"],
        "subject": "Help with my account",
        "body": "Hi, I need help with my account settings. Can you assist?",
    }


@pytest.fixture
def legal_threat_email():
    return {
        "message_id": "<legal-001@lawfirm.com>",
        "sender": "attorney@lawfirm.com",
        "sender_name": "John Attorney",
        "recipients": ["legal@sentinelai.com"],
        "subject": "Cease and Desist Notice",
        "body": "This is a formal cease and desist notice. Our client will pursue legal action and file a lawsuit if you do not comply within 30 days.",
    }


@pytest.fixture
def ransomware_email():
    return {
        "message_id": "<ransom-001@darkweb.com>",
        "sender": "hacker@darkweb.com",
        "recipients": ["admin@sentinelai.com"],
        "subject": "Your files have been encrypted",
        "body": "All your files have been encrypted. Send 5 BTC to bitcoin wallet bc1q123 within 72 hours or your data will be deleted. The decryption key will be destroyed after the deadline.",
    }
