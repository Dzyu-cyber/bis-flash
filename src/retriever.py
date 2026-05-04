import re
import json
from typing import List, Dict, Any, Optional
from collections import OrderedDict

from src.embeddings import embed_query
from src.data_extraction import STANDARD_ID_PATTERN
from src.config import DEFAULT_K, HYBRID_SEARCH_OVERFETCH, MASTER_STANDARDS_PATH
from src.logger import get_logger

logger = get_logger(__name__)

# Cache for master standards
_MASTER_STANDARDS = None

def get_master_standards():
    global _MASTER_STANDARDS
    if _MASTER_STANDARDS is None:
        try:
            if MASTER_STANDARDS_PATH.exists():
                with open(MASTER_STANDARDS_PATH, 'r') as f:
                    _MASTER_STANDARDS = json.load(f)
            else:
                _MASTER_STANDARDS = []
        except Exception as e:
            logger.error(f"Failed to load master standards: {e}")
            _MASTER_STANDARDS = []
    return _MASTER_STANDARDS

def recover_full_id(std_id: str, text: str) -> str:
    """
    Attempts to recover the full standard ID (including year and part) 
    by checking the text and cross-referencing with master_standards.json
    """
    master = get_master_standards()
    if not master:
        return std_id
        
    # Normalize input ID for comparison (remove spaces, dots, colons)
    clean_id = re.sub(r'[^a-zA-Z0-9]', '', std_id).lower()
    if not clean_id:
        return std_id
        
    # Find all candidates in master that contain this ID
    # e.g. "is269" should match "IS 269 : 1989"
    candidates = [m for m in master if clean_id in re.sub(r'[^a-zA-Z0-9]', '', m).lower()]
    
    if not candidates:
        return std_id
        
    if len(candidates) == 1:
        return candidates[0]
        
    # Multiple candidates (different years or parts). 
    # Check text for the specific candidate.
    text_clean = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    for cand in candidates:
        cand_clean = re.sub(r'[^a-zA-Z0-9]', '', cand).lower()
        if cand_clean in text_clean:
            return cand
            
    # If still ambiguous, pick the first one or original
    return candidates[0]

# Cache for CrossEncoder to avoid reloading
_CROSS_ENCODER_CACHE: Dict[str, Any] = {}

def retrieve(query: str, collection: Any, model: Any, k: int = DEFAULT_K) -> List[Dict[str, Any]]:
    """Retrieve the top-k most relevant chunks using semantic search."""
    try:
        # Embed the query
        query_embedding = embed_query(query, model)

        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        # Parse results
        chunks = []
        if results and results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                chunks.append({
                    "chunk_id": results["ids"][0][i],
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "standard_id": results["metadatas"][0][i].get("standard_id", "") if results["metadatas"] else "",
                    "standard_title": results["metadatas"][0][i].get("standard_title", "") if results["metadatas"] else "",
                    "category": results["metadatas"][0][i].get("category", "") if results["metadatas"] else "",
                    "source_pages": results["metadatas"][0][i].get("source_pages", ""),
                    "distance": results["distances"][0][i] if results["distances"] else 1.0,
                })
        return chunks
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        return []

def hybrid_retrieve(query: str, collection: Any, model: Any, k: int = DEFAULT_K) -> List[Dict[str, Any]]:
    """Hybrid retrieval: metadata-filtered search for explicit IDs + semantic search."""
    # Pre-compute query embedding to avoid redundant work in loops
    query_embedding = embed_query(query, model)

    # 1. Identify explicit standard IDs in query
    explicit_ids = STANDARD_ID_PATTERN.findall(query)
    explicit_ids_normalized = [re.sub(r'\s+', ' ', sid).strip().upper() for sid in explicit_ids]

    priority_chunks = []
    seen_ids = set()

    # 2. Priority metadata filtering (Batch)
    if explicit_ids_normalized:
        logger.info(f"Detected explicit IDs: {explicit_ids_normalized}")
        try:
            # Single batch query for all explicit IDs using $in operator
            batch_filtered = collection.query(
                query_embeddings=[query_embedding],
                n_results=10,
                where={"standard_id": {"$in": explicit_ids_normalized}},
                include=["documents", "metadatas", "distances"]
            )
            if batch_filtered and batch_filtered["ids"] and batch_filtered["ids"][0]:
                for i in range(len(batch_filtered["ids"][0])):
                    chunk_id = batch_filtered["ids"][0][i]
                    if chunk_id not in seen_ids:
                        seen_ids.add(chunk_id)
                        priority_chunks.append({
                            "chunk_id": chunk_id,
                            "text": batch_filtered["documents"][0][i],
                            "standard_id": batch_filtered["metadatas"][0][i].get("standard_id", ""),
                            "standard_title": batch_filtered["metadatas"][0][i].get("standard_title", ""),
                            "category": batch_filtered["metadatas"][0][i].get("category", ""),
                            "source_pages": batch_filtered["metadatas"][0][i].get("source_pages", ""),
                            "distance": batch_filtered["distances"][0][i] * 0.5,
                        })
        except Exception as e:
            logger.warning(f"Batch metadata query failed: {e}")

            # Try Text Filter (where_document)
            try:
                text_filtered = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=3,
                    where_document={"$contains": std_id},
                    include=["documents", "metadatas", "distances"]
                )
                if text_filtered and text_filtered["ids"] and text_filtered["ids"][0]:
                    for i in range(len(text_filtered["ids"][0])):
                        chunk_id = text_filtered["ids"][0][i]
                        if chunk_id not in seen_ids:
                            seen_ids.add(chunk_id)
                            priority_chunks.append({
                                "chunk_id": chunk_id,
                                "text": text_filtered["documents"][0][i],
                                "standard_id": text_filtered["metadatas"][0][i].get("standard_id", ""),
                                "standard_title": text_filtered["metadatas"][0][i].get("standard_title", ""),
                                "category": text_filtered["metadatas"][0][i].get("category", ""),
                                "source_pages": text_filtered["metadatas"][0][i].get("source_pages", ""),
                                "distance": text_filtered["distances"][0][i] * 0.7, # Boost text matches
                            })
            except Exception: pass

    # 3. Broad semantic search (over-fetch for merging)
    semantic_chunks = []
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=HYBRID_SEARCH_OVERFETCH,
            include=["documents", "metadatas", "distances"]
        )
        if results and results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                semantic_chunks.append({
                    "chunk_id": results["ids"][0][i],
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "standard_id": results["metadatas"][0][i].get("standard_id", "") if results["metadatas"] else "",
                    "standard_title": results["metadatas"][0][i].get("standard_title", "") if results["metadatas"] else "",
                    "category": results["metadatas"][0][i].get("category", "") if results["metadatas"] else "",
                    "source_pages": results["metadatas"][0][i].get("source_pages", ""),
                    "distance": results["distances"][0][i] if results["distances"] else 1.0,
                })
    except Exception as e:
        logger.error(f"Broad semantic retrieval failed: {e}")

    # 4. Merge and deduplicate
    merged = priority_chunks
    for chunk in semantic_chunks:
        if chunk["chunk_id"] not in seen_ids:
            seen_ids.add(chunk["chunk_id"])
            merged.append(chunk)

    # Sort by distance (smaller is better)
    return sorted(merged, key=lambda x: x.get("distance", 1.0))[:HYBRID_SEARCH_OVERFETCH]

def heuristic_rerank(query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Fast reranking based on keyword overlap and ID matching."""
    query_lower = query.lower()
    query_words = set(re.findall(r'\w+', query_lower))
    
    # Extract explicit IDs from query for priority matching
    query_ids = set(STANDARD_ID_PATTERN.findall(query_lower))
    
    for chunk in chunks:
        text_lower = chunk.get("text", "").lower()
        std_id_lower = chunk.get("standard_id", "").lower()
        
        score = 0.0
        
        # 1. Boost for explicit ID match in metadata or text
        for qid in query_ids:
            if qid in std_id_lower:
                score += 5.0
            if qid in text_lower:
                score += 2.0
                
        # 2. Boost for keyword overlap in text
        text_words = set(re.findall(r'\w+', text_lower))
        overlap = query_words.intersection(text_words)
        score += len(overlap) * 0.15
        
        # 3. STRONG Boost for keyword overlap in Title
        title_lower = chunk.get("standard_title", "").lower()
        title_words = set(re.findall(r'\w+', title_lower))
        title_overlap = query_words.intersection(title_words)
        score += len(title_overlap) * 1.5 # Increased from 0.8
        
        # 3b. ULTRA Boost for title substring match
        # If the title (without numbers) is found in the query or vice-versa
        title_clean = re.sub(r'[\d.:\-\(\)]', ' ', title_lower).strip()
        if len(title_clean) > 10 and (title_clean in query_lower or query_lower in title_clean):
            score += 8.0
        
        # 4. Boost for category match
        category_lower = chunk.get("category", "").lower()
        if category_lower != "other" and category_lower in query_lower:
            score += 3.0
            
        # 5. Boost for 'Part' specificity
        # If the query mentions 'part' and the standard ID or text has that part
        if "part" in query_lower:
            part_match = re.search(r'part\s*(\d+)', query_lower)
            if part_match:
                pnum = part_match.group(1)
                if f"part {pnum}" in std_id_lower or f"part {pnum}" in text_lower:
                    score += 4.0
        
        # 6. Technical Section Boost (e.g., storage, testing, silos)
        tech_keywords = {"storage", "silo", "test", "testing", "requirement", "specification", "chemical", "physical", "composition"}
        tech_overlap = query_words.intersection(tech_keywords).intersection(text_words)
        if tech_overlap:
            score += len(tech_overlap) * 2.0
            
        # 7. Demote 'Root' standards if they are just headers and a Part is better
        # If std_id is very short (e.g., 'IS 1489') but query is specific
        if len(std_id_lower.split(':')) == 1 and "(" not in std_id_lower:
             # This is a root standard ID. Give it a slight penalty if the query is descriptive
             if len(query_words) > 5:
                 score -= 1.0

        # 7. Penalize distance (semantic distance from ChromaDB)
        score -= chunk.get("distance", 1.0) * 2.5
        
        chunk["heuristic_score"] = score
        
    return sorted(chunks, key=lambda x: x.get("heuristic_score", 0), reverse=True)

def rerank(query: str, chunks: List[Dict[str, Any]], model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> List[Dict[str, Any]]:
    """Rerank chunks using a CrossEncoder for higher precision."""
    try:
        if model_name not in _CROSS_ENCODER_CACHE:
            from sentence_transformers import CrossEncoder
            logger.info(f"Loading CrossEncoder: {model_name}")
            _CROSS_ENCODER_CACHE[model_name] = CrossEncoder(model_name)
        
        if not chunks:
            return []
            
        model = _CROSS_ENCODER_CACHE[model_name]
        
        # Run heuristic first to get keyword context
        chunks = heuristic_rerank(query, chunks)
        
        pairs = [[query, chunk["text"]] for chunk in chunks]
        scores = model.predict(pairs)
        
        for i, score in enumerate(scores):
            # Combine Neural score (-10 to 10) with Heuristic score
            # Heuristic score is usually 0-15. We weight them.
            chunks[i]["combined_score"] = (float(score) * 1.5) + (chunks[i].get("heuristic_score", 0) * 0.5)
            
        return sorted(chunks, key=lambda x: x.get("combined_score", -999), reverse=True)
    except Exception as e:
        logger.error(f"Reranking failed: {e}")
        return heuristic_rerank(query, chunks)


def extract_top_standards(chunks: List[Dict[str, Any]], k: int = DEFAULT_K) -> List[str]:
    """Extract unique standard IDs from ranked chunks with full ID recovery."""
    seen = set()
    standards = []

    for chunk in chunks:
        std_id = chunk.get("standard_id", "").strip()
        if not std_id:
            continue
            
        # Recover full ID using master list and chunk text
        full_id = recover_full_id(std_id, chunk.get("text", ""))
        
        # Normalize for deduplication
        norm_id = re.sub(r'[^a-zA-Z0-9]', '', full_id).lower()
        
        if norm_id and norm_id not in seen:
            standards.append(full_id)
            seen.add(norm_id)
            
        if len(standards) >= k:
            break
            
    return standards
