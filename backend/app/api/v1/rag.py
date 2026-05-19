"""
SentinelAI — RAG Search Endpoint
"""

from fastapi import APIRouter, Query
from app.schemas.rag import RAGSearchResponse, RAGChunkResult
from app.rag.pipeline import rag_search

router = APIRouter(tags=["RAG"])


@router.get("/rag/search", response_model=RAGSearchResponse)
async def search_knowledge_base(
    q: str = Query(..., min_length=3, description="Search query"),
    top_k: int = Query(5, ge=1, le=20),
):
    """Search the knowledge base using semantic search."""
    result = await rag_search(q, top_k=top_k)

    return RAGSearchResponse(
        query=q,
        results=[
            RAGChunkResult(
                content=r["content"],
                source_file=r["source_file"],
                chunk_index=r["chunk_index"],
                relevance_score=r["relevance_score"],
                metadata=r.get("metadata", {}),
            )
            for r in result["results"]
        ],
        total_results=result["total"],
    )
