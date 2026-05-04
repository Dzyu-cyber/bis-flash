import os
from pathlib import Path

# --- PROJECT PATHS ---
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = PROJECT_ROOT / "raw_data"
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

# --- DATA FILES ---
CHUNKS_PATH = DATA_DIR / "chunks.json"
CHUNKS_META_PATH = DATA_DIR / "chunks_meta.json"
MASTER_STANDARDS_PATH = DATA_DIR / "master_standards.json"
PDF_DATASET_PATH = RAW_DATA_DIR / "dataset.pdf"

# --- MODEL CONFIG ---
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
# Note: BGE models are top-tier for retrieval tasks
GEMINI_MODEL_NAME = "gemini-2.0-flash"

# --- RETRIEVAL CONFIG ---
CHROMA_COLLECTION_NAME = "bis_standards"
DEFAULT_K = 10
HYBRID_SEARCH_OVERFETCH = 50

# --- LOGGING CONFIG ---
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
