"""
SentinelAI — Document Chunker

Recursive text splitting for knowledge base documents.
"""

import re
from dataclasses import dataclass


@dataclass
class Chunk:
    content: str
    source_file: str
    chunk_index: int
    token_count: int
    metadata: dict


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English text."""
    return len(text) // 4


def chunk_document(
    text: str,
    source_file: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    """
    Split a document into overlapping chunks.
    Uses a hierarchy of separators for intelligent splitting.
    """
    separators = ["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
    chunks = _recursive_split(text, separators, chunk_size * 4)  # chars ≈ tokens * 4

    results = []
    for i, chunk_text in enumerate(chunks):
        chunk_text = chunk_text.strip()
        if not chunk_text or len(chunk_text) < 20:
            continue

        results.append(Chunk(
            content=chunk_text,
            source_file=source_file,
            chunk_index=i,
            token_count=estimate_tokens(chunk_text),
            metadata={"source": source_file, "chunk_index": i},
        ))

    return results


def _recursive_split(text: str, separators: list[str], max_chars: int) -> list[str]:
    """Recursively split text using hierarchy of separators."""
    if len(text) <= max_chars:
        return [text]

    # Try each separator
    for sep in separators:
        parts = text.split(sep)
        if len(parts) <= 1:
            continue

        chunks = []
        current = ""

        for part in parts:
            candidate = current + sep + part if current else part

            if len(candidate) > max_chars and current:
                chunks.append(current)
                current = part
            else:
                current = candidate

        if current:
            chunks.append(current)

        # Recursively split any oversized chunks
        result = []
        for chunk in chunks:
            if len(chunk) > max_chars:
                result.extend(_recursive_split(chunk, separators[1:], max_chars))
            else:
                result.append(chunk)

        return result

    # Last resort: hard split
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def chunk_all_documents(knowledge_base_dir: str) -> list[Chunk]:
    """Chunk all markdown files in the knowledge base directory."""
    import os

    all_chunks = []
    for filename in sorted(os.listdir(knowledge_base_dir)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(knowledge_base_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_document(text, filename)
        all_chunks.extend(chunks)

    return all_chunks
