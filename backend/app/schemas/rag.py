"""
SentinelAI — RAG Schemas
"""

from pydantic import BaseModel, Field


class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)


class RAGChunkResult(BaseModel):
    content: str
    source_file: str
    chunk_index: int
    relevance_score: float
    metadata: dict = {}


class RAGSearchResponse(BaseModel):
    query: str
    results: list[RAGChunkResult]
    total_results: int
