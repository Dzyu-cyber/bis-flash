"""
embeddings.py — Embedding generation and ChromaDB vector database management.

Uses local BGE models for zero-latency embeddings and ChromaDB for persistent storage.
"""

import json
from typing import List, Dict, Tuple, Any
# from sentence_transformers import SentenceTransformer # Moved inside functions
import chromadb
from src.config import (
    EMBEDDING_MODEL_NAME, 
    CHROMA_DB_DIR, 
    CHROMA_COLLECTION_NAME
)
from src.logger import get_logger

logger = get_logger(__name__)

# BGE models benefit from instruction prefixes for queries
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

def get_embedding_model(model_name: str = EMBEDDING_MODEL_NAME):
    """Load the embedding model."""
    print(f"DEBUG: Calling SentenceTransformer('{model_name}')")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name, device='cpu')
        print(f"DEBUG: Model loaded.")
        logger.info(f"Model loaded. Dimension: {model.get_sentence_embedding_dimension()}")
        return model
    except Exception as e:
        logger.error(f"Failed to load embedding model: {e}")
        raise

def embed_chunks(chunks: List[Dict[str, Any]], model: Any, batch_size: int = 32) -> List[Dict[str, Any]]:
    """Generate embeddings for all chunks."""
    texts = [chunk["text"] for chunk in chunks]
    logger.info(f"Embedding {len(texts)} chunks (batch_size={batch_size})...")
    
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    logger.info(f"Successfully embedded {len(chunks)} chunks")
    return chunks

def embed_query(query: str, model: Any) -> List[float]:
    """Embed a single query with the BGE instruction prefix."""
    prefixed_query = BGE_QUERY_PREFIX + query
    embedding = model.encode(
        prefixed_query,
        normalize_embeddings=True
    )
    return embedding.tolist()

def init_chroma_collection(
    persist_dir: str = str(CHROMA_DB_DIR),
    collection_name: str = CHROMA_COLLECTION_NAME
) -> Tuple[chromadb.PersistentClient, Any]:
    """Initialize or load a persistent ChromaDB collection."""
    logger.info(f"Initializing ChromaDB at {persist_dir}...")
    client = chromadb.PersistentClient(path=persist_dir)

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    logger.info(f"Collection '{collection_name}' ready. Count: {collection.count()}")
    return client, collection

def upsert_to_chroma(collection: Any, chunks: List[Dict[str, Any]]):
    """Upsert embedded chunks into ChromaDB with metadata."""
    if not chunks:
        logger.warning("No chunks provided for upsert")
        return

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        embeddings.append(chunk["embedding"])
        documents.append(chunk["text"])
        metadatas.append({
            "standard_id": chunk.get("standard_id", ""),
            "standard_title": chunk.get("standard_title", "")[:500],
            "category": chunk.get("category", ""),
            "source_pages": str(chunk.get("source_pages", [])),
        })

    # Upsert in batches
    batch_size = 5000
    for i in range(0, len(ids), batch_size):
        end = min(i + batch_size, len(ids))
        collection.upsert(
            ids=ids[i:end],
            embeddings=embeddings[i:end],
            documents=documents[i:end],
            metadatas=metadatas[i:end]
        )

    logger.info(f"Upserted {len(ids)} chunks. New total: {collection.count()}")
