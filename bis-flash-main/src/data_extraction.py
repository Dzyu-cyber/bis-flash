"""
data_extraction.py — PDF parsing and preprocessing for BIS SP 21 documents.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Set

import pdfplumber
from src.config import MASTER_STANDARDS_PATH
from src.logger import get_logger

logger = get_logger(__name__)

# Pattern for BIS standard IDs: IS 269, IS 269: 1989, IS 2185 (Part 2): 1983, etc.
STANDARD_ID_PATTERN = re.compile(
    r'IS(?:\s*/\s*ISO)?\s*\d{1,5}(?:\s*\(\s*Part\s*(?:\d+|[IVXLC]+)\s*\))?\s*(?::\s*\d{4})?',
    re.IGNORECASE
)

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract text and tables from a PDF page by page."""
    pages = []
    logger.info(f"Opening PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                tables = page.extract_tables() or []
                
                pages.append({
                    "text": text,
                    "page": i + 1,
                    "raw_tables": tables
                })
        logger.info(f"Extracted {len(pages)} pages.")
        return pages
    except Exception as e:
        logger.error(f"Failed to extract PDF text: {e}")
        return []

def clean_text(raw_text: str) -> str:
    """Clean extracted text by removing noise and normalizing whitespace."""
    text = raw_text
    # Remove CID artifacts
    text = re.sub(r'\(cid:\d+\)', ' ', text)
    # Remove standalone page numbers
    text = re.sub(r'(?m)^\s*\d{1,4}\s*$', '', text)
    
    # Remove BIS-specific noise
    patterns = [
        r'BUREAU OF INDIAN STANDARDS',
        r'SP\s*21\s*:\s*1983',
        r'HANDBOOK\s*ON\s*SUMMARIES\s*OF\s*INDIAN\s*STANDARDS\s*FOR\s*BUILDING\s*MATERIALS',
        r'FOR\s*INTERNAL\s*USE\s*ONLY',
        r'COURTESY\s*COPY',
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = '\n'.join(line.strip() for line in text.split('\n'))
    return text.strip()

def tables_to_text(raw_tables: List[Any]) -> str:
    """Convert table data into natural language sentences."""
    if not raw_tables:
        return ""

    parts = []
    for table in raw_tables:
        if not table or len(table) < 1:
            continue

        if len(table) == 1:
            row = [str(cell).strip() if cell else "" for cell in table[0]]
            parts.append(" ".join(row))
            continue

        headers = [str(cell).strip() if cell else f"Col {j+1}" for j, cell in enumerate(table[0])]
        for row in table[1:]:
            cells = [str(cell).strip() if cell else "" for cell in row]
            pairs = [f"{h}: {c}" for h, c in zip(headers, cells) if h and c and c.lower() not in ('', 'none', '-', 'nil')]
            if pairs:
                parts.append("; ".join(pairs))

    return "\n".join(parts)

def extract_standard_ids(text: str) -> List[str]:
    """Extract and normalize unique standard IDs from text."""
    matches = STANDARD_ID_PATTERN.findall(text)
    cleaned = [re.sub(r'\s+', ' ', m).strip() for m in matches]
    
    unique = []
    seen = set()
    for s in cleaned:
        norm = re.sub(r'\s+', '', s).lower()
        if norm not in seen:
            seen.add(norm)
            unique.append(s)
    return unique

def process_pdf(pdf_path: str) -> Dict[str, Any]:
    """Full extraction pipeline: PDF -> Cleaned Pages + Master List."""
    raw_pages = extract_text_from_pdf(pdf_path)
    cleaned_pages = []
    all_standards = set()

    logger.info("Cleaning text and processing tables...")
    for page in raw_pages:
        txt = clean_text(page["text"])
        tbl = tables_to_text(page["raw_tables"])
        full_text = f"{txt}\n\n[TABLE DATA]\n{tbl}" if tbl else txt
        
        std_ids = extract_standard_ids(full_text)
        all_standards.update(std_ids)

        cleaned_pages.append({
            "text": full_text,
            "page": page["page"],
            "standard_ids": std_ids
        })

    master_standards = sorted(list(all_standards))
    
    # Save master standards
    with open(MASTER_STANDARDS_PATH, "w", encoding="utf-8") as f:
        json.dump(master_standards, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(master_standards)} standards to {MASTER_STANDARDS_PATH}")
    return {
        "pages": cleaned_pages,
        "master_standards": master_standards
    }
