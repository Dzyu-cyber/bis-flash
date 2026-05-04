"""
generator.py — LLM integration for generating human-readable rationale and query expansion.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai

from src.config import GEMINI_MODEL_NAME
from src.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def init_gemini() -> genai.GenerativeModel:
    """Initialize the Gemini LLM client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment.")
        raise ValueError("GEMINI_API_KEY not found in environment. Set it in .env")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL_NAME,
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 1024,
        }
    )

    logger.info(f"Gemini initialized with model: {GEMINI_MODEL_NAME}")
    return model

def _parse_json_response(text: str) -> Any:
    """Helper to parse JSON from LLM response, handling markdown blocks."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}. Raw text: {text}")
        raise

def generate_rationale(query: str, standards: List[str], chunks: List[Dict[str, Any]], model: genai.GenerativeModel, lang: str = "en") -> List[Dict[str, Any]]:
    """Generate human-readable rationale for each recommended standard in the specified language."""
    context_parts = []
    standards_set = {s.strip().lower() for s in standards}
    
    # Map from normalized to original for matching
    norm_to_orig = {s.strip().lower(): s for s in standards}
    
    for chunk in chunks:
        # Some chunks might have 'metadata' with 'standard_id' or direct 'standard_id'
        std_id = chunk.get("metadata", {}).get("standard_id", "") or chunk.get("standard_id", "")
        if std_id and std_id.strip().lower() in standards_set:
            text = chunk.get("content", "") or chunk.get("text", "")
            context_parts.append(f"--- {std_id} ---\n{text[:1000]}")

    context = "\n\n".join(context_parts)
    
    lang_name = {
        "en": "English",
        "hi": "Hindi (हिंदी)",
        "te": "Telugu (తెలుగు)"
    }.get(lang, "English")

    prompt = f"""You are a BIS (Bureau of Indian Standards) compliance expert.
Your task is to explain which Indian Standards apply to a specific product or technical need.

User Query: "{query}"

Target Language: {lang_name}

Identified Standards:
{json.dumps(standards)}

Documentation Context:
{context}

For each standard in the 'Identified Standards' list, provide:
1. The standard ID (exactly as given in the list)
2. The full technical title of the standard (in {lang_name})
3. A detailed summary of the standard's scope (in {lang_name}, 2 sentences)
4. A clear rationale explaining why this standard is relevant to the user's specific query (in {lang_name}, 2-3 sentences)

Respond in this exact JSON format (a list of objects):
[
  {{
    "standard_id": "IS 269: 1989",
    "title": "...",
    "summary": "...",
    "rationale": "..."
  }}
]

IMPORTANT:
- Translate all fields except "standard_id" into {lang_name}.
- Only include standards from the provided list.
- If context is missing for a standard, use your internal knowledge to provide the title and a generic but accurate rationale.
"""

    try:
        response = model.generate_content(prompt)
        return _parse_json_response(response.text)
    except Exception as e:
        logger.error(f"Error generating rationale: {e}")
        return [
            {
                "standard_id": s, 
                "title": f"BIS Standard {s}", 
                "summary": "Technical specifications for product compliance.",
                "rationale": "Identified as highly relevant based on semantic match with your query."
            }
            for s in standards
        ]

def identify_standards(query: str, chunks: List[Dict[str, Any]], model: genai.GenerativeModel) -> List[str]:
    """Use Gemini to identify and rank the top applicable standards from excerpts."""
    context_parts = [
        f"Excerpt {i+1} [Source: {c.get('standard_id', 'Unknown')}]:\n{c.get('text', '')}"
        for i, c in enumerate(chunks[:10])
    ]
    
    context = "\n\n".join(context_parts)
    
    prompt = f"""You are a BIS (Bureau of Indian Standards) compliance expert.

A user described their product/need:
"{query}"

Based on the official BIS document excerpts provided below, identify the top 3-5 most applicable Indian Standards.

RULES:
1. Return ONLY standard IDs that appear in the provided excerpts (Source tags)
2. Format each as "IS XXXX: YYYY" or "IS XXXX (Part N): YYYY"
3. Rank by relevance — most applicable standard FIRST
4. Do NOT invent or guess standard IDs
5. Respond in strict JSON array format: ["IS 269: 1989", "IS 455: 1989", ...]

EXCERPTS:
{context}

Response (JSON array only):"""

    try:
        response = model.generate_content(prompt)
        standards = _parse_json_response(response.text)
        if isinstance(standards, list):
            return [str(s).strip() for s in standards]
    except Exception as e:
        logger.error(f"Identification failed: {e}")
        # Fallback to simple extraction
        matches = re.findall(r'IS\s*\d+(?:\s*\(Part\s*\d+\))?\s*(?::\s*\d{4})?', response.text if 'response' in locals() else "")
        return list(dict.fromkeys(matches))

    return []

def expand_query(query: str, model: genai.GenerativeModel) -> str:
    """Expand user query with technical terminology for improved retrieval."""
    prompt = f"""You are a BIS standards expert. Rewrite this query to include relevant technical terms, 
material types, and BIS-related keywords that would help find the correct standard. 
Keep it as a single search query (not a list). Max 2 sentences. No standard numbers.

Original query: "{query}"

Expanded query:"""

    try:
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                expanded = response.text.strip()
                return f"{query} {expanded}"
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5
                    logger.warning(f"Rate limited (429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise e
    except Exception as e:
        logger.error(f"Query expansion failed: {e}")
        return query
