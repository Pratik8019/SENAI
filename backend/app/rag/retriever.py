"""
SentinelAI — Vector Retriever

ChromaDB-based vector search for RAG pipeline.
"""

import chromadb
from app.core.config import get_settings
from app.rag.embeddings import generate_embedding

settings = get_settings()

COLLECTION_NAME = "sentinel_knowledge_base"


def get_chroma_client() -> chromadb.HttpClient:
    return chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port,
    )


def get_or_create_collection(client: chromadb.HttpClient = None):
    if client is None:
        client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


async def search(
    query: str,
    top_k: int = 5,
    relevance_threshold: float = 0.3,
) -> list[dict]:
    """
    Semantic search against the knowledge base.
    Returns ranked results with relevance scores and source citations.
    """
    try:
        collection = get_or_create_collection()
        query_embedding = await generate_embedding(query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        if not results or not results["documents"] or not results["documents"][0]:
            return []

        search_results = []
        for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            # ChromaDB cosine distance → similarity score
            relevance = 1.0 - distance

            if relevance < relevance_threshold:
                continue

            search_results.append({
                "content": doc,
                "source_file": meta.get("source_file", "unknown"),
                "chunk_index": meta.get("chunk_index", 0),
                "relevance_score": round(relevance, 4),
                "metadata": meta,
            })

        return search_results

    except Exception as e:
        # Graceful fallback if ChromaDB is unavailable
        return []


async def index_chunks(chunks: list[dict]) -> int:
    """Index document chunks into ChromaDB."""
    try:
        collection = get_or_create_collection()

        ids = [f"{c['source_file']}_{c['chunk_index']}" for c in chunks]
        documents = [c["content"] for c in chunks]
        metadatas = [
            {"source_file": c["source_file"], "chunk_index": c["chunk_index"]}
            for c in chunks
        ]

        from app.rag.embeddings import generate_embeddings_batch
        embeddings = await generate_embeddings_batch(documents)

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(ids)
    except Exception as e:
        raise RuntimeError(f"Failed to index chunks: {e}")
