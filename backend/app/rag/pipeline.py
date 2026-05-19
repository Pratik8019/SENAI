"""
SentinelAI — RAG Pipeline Orchestrator

Combines chunking, embedding, retrieval, and context formatting.
"""

from app.rag.retriever import search
from app.rag.chunker import chunk_all_documents
from app.rag.retriever import index_chunks


async def rag_search(query: str, top_k: int = 5) -> dict:
    """
    Full RAG search: query → embed → retrieve → format with citations.
    """
    results = await search(query, top_k=top_k)

    formatted_context = ""
    citations = []

    for r in results:
        formatted_context += (
            f"\n--- Source: {r['source_file']} (relevance: {r['relevance_score']}) ---\n"
            f"{r['content']}\n"
        )
        citations.append({
            "source": r["source_file"],
            "relevance": r["relevance_score"],
            "chunk_index": r["chunk_index"],
        })

    return {
        "context": formatted_context,
        "citations": citations,
        "results": results,
        "total": len(results),
    }


async def index_knowledge_base(kb_dir: str) -> int:
    """Index all documents in the knowledge base directory."""
    chunks = chunk_all_documents(kb_dir)

    chunk_dicts = [
        {
            "content": c.content,
            "source_file": c.source_file,
            "chunk_index": c.chunk_index,
        }
        for c in chunks
    ]

    count = await index_chunks(chunk_dicts)
    return count
