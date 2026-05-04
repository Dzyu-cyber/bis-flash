import logging
import sys
from src.config import LOG_FORMAT, LOG_LEVEL

def get_logger(name: str):
    """Returns a logger with a consistent format and level."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
        
    return logger
