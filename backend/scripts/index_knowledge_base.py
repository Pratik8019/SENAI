"""
SentinelAI — Knowledge Base Indexer

Indexes all RAG documents into ChromaDB.
"""

import asyncio
import os
from app.rag.pipeline import index_knowledge_base


async def main():
    kb_dir = os.path.join(os.path.dirname(__file__), "..", "app", "rag", "knowledge_base")
    kb_dir = os.path.abspath(kb_dir)

    print(f"📚 Indexing knowledge base from: {kb_dir}")
    count = await index_knowledge_base(kb_dir)
    print(f"✅ Indexed {count} chunks into ChromaDB")


if __name__ == "__main__":
    asyncio.run(main())
