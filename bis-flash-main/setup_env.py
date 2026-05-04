import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Setup")

def run_command(command):
    logger.info(f"Running: {command}")
    try:
        subprocess.check_call([sys.executable, "-m"] + command.split())
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        return False
    return True

def setup():
    logger.info("Starting Environment Setup for BIS Standards RAG Engine...")
    
    # 1. Install requirements
    if not run_command("pip install -r requirements.txt"):
        logger.error("Failed to install requirements.")
        return

    # 2. Pre-cache models
    logger.info("Pre-caching models (Embedding and Reranker)...")
    try:
        from sentence_transformers import SentenceTransformer, CrossEncoder
        from src.config import EMBEDDING_MODEL_NAME
        
        logger.info(f"Downloading Embedding Model: {EMBEDDING_MODEL_NAME}")
        SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        logger.info("Downloading Neural Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2")
        CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        
        logger.info("Models cached successfully.")
    except Exception as e:
        logger.error(f"Failed to cache models: {e}")
        return

    # 3. Check for index
    from src.config import CHROMA_DB_DIR
    if not os.path.exists(CHROMA_DB_DIR) or not os.listdir(CHROMA_DB_DIR):
        logger.info("ChromaDB index not found. Building index (this may take a few minutes)...")
        if not run_command("python build_index.py"):
            logger.error("Failed to build index.")
            return
    else:
        logger.info("ChromaDB index already exists.")

    logger.info("====================================================")
    logger.info("SETUP COMPLETE! Your environment is ready.")
    logger.info("Run evaluation with: python inference.py --input data/public_test_set.json")
    logger.info("====================================================")

if __name__ == "__main__":
    setup()
