"""
chunking.py — Standard-aware chunking strategy for BIS standards documents.
"""

import re
import json
import hashlib
from typing import List, Dict, Any, Optional
from src.logger import get_logger
from src.data_extraction import STANDARD_ID_PATTERN

logger = get_logger(__name__)

def _generate_chunk_id(standard_id: str, chunk_index: int) -> str:
    """Generate a deterministic chunk ID."""
    raw = f"{standard_id}_{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]

def _detect_category(text: str, current_section: Optional[str] = None) -> str:
    """Detect product category from text or current section."""
    if current_section:
        return current_section

    text_lower = text.lower()
    categories = [
        ("Aggregates", ["aggregate", "sand", "gravel"]),
        ("Cement", ["cement", "opc", "portland"]),
        ("Steel", ["steel", "reinforcement", "bar"]),
        ("Concrete", ["concrete", "rcc", "precast"]),
        ("Masonry", ["masonry", "brick", "block"]),
        ("Pipes", ["pipe", "drain"]),
        ("Roofing", ["roofing", "sheet", "tile"]),
    ]
    for category, keywords in categories:
        if any(kw in text_lower for kw in keywords):
            return category
    return "Other"

def _detect_section_header(para: str) -> Optional[str]:
    """Detect if a paragraph is a section header."""
    para_upper = para.strip().upper()
    sections = {
        "CEMENT": "Cement", "CONCRETE": "Concrete", "AGGREGATES": "Aggregates",
        "STEEL": "Steel", "MASONRY": "Masonry", "PIPES": "Pipes",
        "ROOFING": "Roofing", "WOOD": "Wood Products", "LIME": "Limes"
    }
    
    match = re.search(r'SECTION\s+\d+\s+([A-Z\s&,]+)', para_upper)
    if match:
        name = match.group(1).strip()
        for k, v in sections.items():
            if k in name: return v
        return name.title()

    if len(para_upper) < 40:
        for k, v in sections.items():
            if k == para_upper: return v
                
    return None

def _extract_title(text: str, standard_id: str) -> str:
    """Extract standard title from text."""
    pattern = re.escape(standard_id) + r'\s*[-—:]?\s*(.+?)(?:\n|$)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        title = re.sub(r'(?i)\(?(?:first|second|third|fourth|fifth)?\s*revision\)?', '', title)
        title = re.sub(r'(?i)specification for\s*', '', title)
        return re.sub(r'\s+', ' ', title).strip()[:120]
    return standard_id

def chunk_by_standard(pages: List[Dict[str, Any]], max_tokens: int = 800) -> List[Dict[str, Any]]:
    """Group text by standard ID and create chunks with more robustness."""
    standard_texts = {}
    current_section = "General"
    
    logger.info("Extracting standards and building context-aware chunks...")

    for page in pages:
        text = page.get("text", "")
        page_num = page.get("page", 0)
        
        # Detect Section
        for line in text.split('\n')[:10]: # Check first few lines for section headers
            section = _detect_section_header(line)
            if section:
                current_section = section
                break

        # Find all standard IDs on this page
        ids_on_page = STANDARD_ID_PATTERN.findall(text)
        if not ids_on_page:
            continue

        # Normalize IDs found
        page_standards = []
        for raw_id in ids_on_page:
            norm_id = re.sub(r'\s+', ' ', raw_id).strip().upper()
            page_standards.append(norm_id)

        # For each standard on the page, the whole page (or relevant part) is its context
        # This is redundant but ensures maximum retrieval coverage
        for std_id in set(page_standards):
            if std_id not in standard_texts:
                standard_texts[std_id] = {"texts": [], "pages": [], "section": current_section}
            
            # Add the page text as a block for this standard
            standard_texts[std_id]["texts"].append(text)
            standard_texts[std_id]["pages"].append(page_num)

    # Convert groups to chunks
    chunks = []
    for std_id, data in standard_texts.items():
        # Combine all pages where this standard appeared
        combined_text = '\n\n[...]\n\n'.join(data["texts"])
        
        # If it's too huge, just take the first 2000 chars around the standard mention
        # (This is a simplification, but effective for retrieval)
        title = _extract_title(combined_text, std_id)
        category = _detect_category(combined_text, data["section"])
        
        # Deduplicate and limit size for vector DB
        chunks.append({
            "chunk_id": _generate_chunk_id(std_id, 0),
            "text": combined_text[:4000], # Keep a good amount of context
            "standard_id": std_id,
            "standard_title": title,
            "category": category,
            "source_pages": sorted(set(data["pages"]))
        })

    logger.info(f"Created {len(chunks)} chunks covering {len(standard_texts)} unique standards.")
    return chunks

def add_context_headers(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add synthetic headers to improve embedding quality."""
    for chunk in chunks:
        header = f"[{chunk['standard_id']} — {chunk['standard_title']} — {chunk['category']}]"
        chunk["text"] = f"{header}\n{chunk['text']}"
    return chunks
