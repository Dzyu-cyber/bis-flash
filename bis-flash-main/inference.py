"""
inference.py — Entry-point for evaluation.
"""

import argparse
import json
import time
import sys
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import RAGPipeline
from src.logger import get_logger

logger = get_logger("Inference")

def main():
    parser = argparse.ArgumentParser(description="BIS Standards Recommendation Engine — Inference Script")
    parser.add_argument("--input", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output", type=str, required=True, help="Path to save output JSON file")
    parser.add_argument("--no-expand", action="store_true", help="Disable LLM query expansion for speed")
    args = parser.parse_args()

    # Load input queries
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            queries = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load input file: {e}")
        return

    # Initialize Pipeline
    pipeline = RAGPipeline(use_llm_expansion=not args.no_expand)

    results = []
    logger.info(f"Processing {len(queries)} queries...")
    
    for i, item in enumerate(queries):
        query_id = item.get("id", "unknown")
        query_text = item.get("query", "")
        
        logger.info(f"[{i+1}/{len(queries)}] Processing query: {query_id}")
        
        # Process query with zero artificial delay for maximum performance score

            
        try:
            start = time.perf_counter()
            # use_llm_id=False for fastest, zero-hallucination scoring
            retrieved = pipeline.run(query_text, use_llm_id=False, expand=not args.no_expand)
            latency = round(time.perf_counter() - start, 4)
            
            logger.info(f"Query {query_id} finished in {latency}s. Found {len(retrieved)} standards.")

            results.append({
                "id": query_id,
                "query": query_text,
                "expected_standards": item.get("expected_standards", []),
                "retrieved_standards": retrieved,
                "latency_seconds": latency
            })
        except Exception as e:
            logger.error(f"Query {query_id} failed: {e}")
            results.append({
                "id": query_id,
                "query": query_text,
                "expected_standards": item.get("expected_standards", []),
                "retrieved_standards": [],
                "latency_seconds": 0.0
            })

    # Save results
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully processed {len(results)} queries. Output: {args.output}")

if __name__ == "__main__":
    main()
