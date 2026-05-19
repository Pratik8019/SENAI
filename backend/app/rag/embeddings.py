"""
SentinelAI — Embedding Generator

Generate embeddings using OpenAI or fallback to simple TF-IDF-style hashing.
"""

import hashlib
import struct
from openai import AsyncOpenAI
from app.core.config import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


async def generate_embedding(text: str) -> list[float]:
    """Generate embedding vector for text."""
    if client and settings.openai_api_key:
        return await _openai_embedding(text)
    return _fallback_embedding(text)


async def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Batch embedding generation."""
    if client and settings.openai_api_key:
        return await _openai_batch_embeddings(texts)
    return [_fallback_embedding(t) for t in texts]


async def _openai_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=text,
    )
    return response.data[0].embedding


async def _openai_batch_embeddings(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [d.embedding for d in response.data]


def _fallback_embedding(text: str, dim: int = 384) -> list[float]:
    """
    Deterministic hash-based pseudo-embedding for when OpenAI is not available.
    NOT suitable for production semantic search — only for testing/demo.
    """
    h = hashlib.sha512(text.encode()).digest()
    # Extend hash to fill dimensions
    extended = h * (dim // len(h) + 1)
    values = struct.unpack(f"{dim}B", extended[:dim])
    # Normalize to [-1, 1]
    return [(v / 127.5) - 1.0 for v in values]
