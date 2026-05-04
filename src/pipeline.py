"""
pipeline.py — End-to-end RAG pipeline orchestration for BIS Standards.
"""

import re
import json
from typing import List, Tuple, Set, Dict, Any, Optional

from src.embeddings import get_embedding_model, init_chroma_collection
from src.retriever import hybrid_retrieve, extract_top_standards, rerank
from src.generator import init_gemini, expand_query, identify_standards
from src.config import MASTER_STANDARDS_PATH, DEFAULT_K
from src.logger import get_logger

logger = get_logger(__name__)

class RAGPipeline:
    """Main orchestration class for the RAG pipeline."""

    def __init__(self, use_llm_expansion: bool = True):
        """Initialize models and database connections."""
        self.model = get_embedding_model()
        self.client, self.collection = init_chroma_collection()
        self.master_standards = self._load_master_standards()
        self.llm = None
        if use_llm_expansion:
            try:
                self.llm = init_gemini()
            except Exception as e:
                logger.warning(f"Gemini initialization failed (expansion disabled): {e}")

        # Pre-load reranker to avoid latency spikes on first query
        try:
            logger.info("Pre-loading neural reranker...")
            rerank("pre-load", [])
        except: pass

        logger.info(f"Pipeline initialized. ChromaDB count: {self.collection.count()}")

    def _normalize(self, s: str) -> str:
        """Shared normalization logic for standards."""
        # Remove all non-alphanumeric
        s = re.sub(r'[^a-z0-9]', '', s.lower())
        # Standardize Roman Part I/II/III to Part 1/2/3 for matching
        s = s.replace('partiv', 'part4')
        s = s.replace('partiii', 'part3')
        s = s.replace('partii', 'part2')
        s = s.replace('parti', 'part1')
        return s

    def _load_master_standards(self) -> Set[str]:
        """Load and normalize the master standards list for validation."""
        if MASTER_STANDARDS_PATH.exists():
            with open(MASTER_STANDARDS_PATH, "r", encoding="utf-8") as f:
                standards = json.load(f)
            return {self._normalize(s) for s in standards}
        logger.warning(f"Master standards file not found at {MASTER_STANDARDS_PATH}")
        return set()

    def _validate_standards(self, standards: List[str]) -> List[str]:
        """Filter out standards not in the master list with fuzzy/prefix matching."""
        if not self.master_standards:
            return standards
            
        validated = []
        seen_norm = set()
        for std in standards:
            norm = self._normalize(std)
            if norm in seen_norm:
                continue

            # Exact match
            if norm in self.master_standards:
                validated.append(std)
                seen_norm.add(norm)
            else:
                # Fuzzy/Prefix match (e.g., IS 303 matches IS 303:1989)
                is_valid = False
                for master_norm in self.master_standards:
                    if master_norm.startswith(norm) or norm.startswith(master_norm):
                        is_valid = True
                        break
                
                if is_valid:
                    validated.append(std)
                    seen_norm.add(norm)
                else:
                    logger.info(f"Hallucination Filter: Removed unknown standard '{std}'")
        return validated

    def run(self, query: str, k: int = DEFAULT_K, use_llm_id: bool = False, expand: bool = True) -> List[str]:
        """Run the core retrieval pipeline."""
        search_query = query
        if self.llm and expand:
            search_query = expand_query(query, self.llm)

        chunks = hybrid_retrieve(
            query=search_query,
            collection=self.collection,
            model=self.model,
            k=k * 2
        )

        # 1. Fast heuristic rerank on all overfetched chunks
        from src.retriever import heuristic_rerank
        chunks = heuristic_rerank(query=search_query, chunks=chunks)
        
        # 2. Neural rerank on top 12 candidates for sub-5s performance
        chunks = rerank(query=search_query, chunks=chunks[:12])

        if use_llm_id and self.llm:
            standards = identify_standards(query, chunks, self.llm)
        else:
            standards = extract_top_standards(chunks, k=k)

        return self._validate_standards(standards)[:k]

    def run_with_details(self, query: str, k: int = DEFAULT_K, lang: str = "en") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Run the pipeline and return both detailed standards and source chunks."""
        search_query = query
        # Always expand query for better semantic match
        if self.llm:
            search_query = expand_query(query, self.llm)

        chunks = hybrid_retrieve(
            query=search_query,
            collection=self.collection,
            model=self.model,
            k=20
        )

        # 1. Fast heuristic rerank on all overfetched chunks
        from src.retriever import heuristic_rerank
        chunks = heuristic_rerank(query=search_query, chunks=chunks)
        
        # 2. Neural rerank on top 12 candidates for sub-5s performance
        chunks = rerank(query=search_query, chunks=chunks[:12])
        
        # 3. Identify standards from chunks
        standards_ids = extract_top_standards(chunks, k=k)
        validated_standards = self._validate_standards(standards_ids)
        
        # 4. Generate high-quality rationales in the target language
        if self.llm:
            from src.generator import generate_rationale
            results = generate_rationale(query, validated_standards, chunks, self.llm, lang=lang)
        else:
            # Fallback if LLM is not available
            results = [
                {
                    "standard_id": std,
                    "title": f"BIS Standard {std}",
                    "summary": "Details about this standard.",
                    "rationale": f"Identified based on semantic match with query: {query}"
                }
                for std in validated_standards
            ]
        
        return results, chunks
