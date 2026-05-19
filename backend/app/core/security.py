"""
SentinelAI — Security Utilities

JWT token management, password hashing, and prompt injection protection.
"""

import re
import hashlib
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def hash_message_id(message_id: str) -> str:
    return hashlib.sha256(message_id.encode()).hexdigest()


# Prompt injection protection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?prior",
    r"you\s+are\s+now\s+",
    r"new\s+instructions?:",
    r"system\s*prompt:",
    r"<\|im_start\|>",
    r"\[INST\]",
    r"```\s*system",
]

_injection_regex = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)


def sanitize_input(text: str) -> str:
    """Remove potential prompt injection patterns from user input."""
    cleaned = _injection_regex.sub("[FILTERED]", text)
    # Strip control characters
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", cleaned)
    return cleaned.strip()


def detect_injection(text: str) -> bool:
    """Returns True if the text contains suspected prompt injection."""
    return bool(_injection_regex.search(text))
