"""
build_index.py — One-shot script to build the entire vector index.
"""

import time
import sys
import os
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import PDF_DATASET_PATH, CHUNKS_PATH
from src.data_extraction import process_pdf
from src.chunking import chunk_by_standard, add_context_headers
from src.embeddings import get_embedding_model, embed_chunks, init_chroma_collection, upsert_to_chroma
from src.logger import get_logger

logger = get_logger("IndexBuilder")

def main():
    start_time = time.perf_counter()
    logger.info("Starting index build process...")

    try:
        # 1. Extraction
        if not PDF_DATASET_PATH.exists():
            logger.error(f"PDF not found at {PDF_DATASET_PATH}. Please place the dataset there.")
            return

        result = process_pdf(str(PDF_DATASET_PATH))
        pages = result["pages"]

        # 2. Chunking
        chunks = chunk_by_standard(pages)
        chunks = add_context_headers(chunks)
        
        # Save chunks for debugging/reference
        import json
        with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        # 3. Embedding & Indexing
        model = get_embedding_model()
        chunks = embed_chunks(chunks, model)

        client, collection = init_chroma_collection()
        upsert_to_chroma(collection, chunks)

        elapsed = time.perf_counter() - start_time
        logger.info(f"Build complete in {elapsed:.1f}s. Total chunks: {collection.count()}")
    except Exception as e:
        logger.exception(f"Index build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
