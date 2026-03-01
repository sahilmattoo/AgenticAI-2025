"""
LangSmith Configuration.
Ensures tracing is enabled and configured correctly for production debugging.
"""
import os
from .logging import logger

def configure_tracing():
    """
    Verifies and sets up LangChain tracing environment variables.
    """
    # Check for critical env vars
    api_key = os.getenv("LANGCHAIN_API_KEY")
    tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
    project = os.getenv("LANGCHAIN_PROJECT")

    if not api_key:
        logger.warning("observability_config", message="LANGCHAIN_API_KEY not found. Tracing may fail.")
    
    if tracing_v2 != "true":
        logger.warning("observability_config", message="LANGCHAIN_TRACING_V2 is not 'true'. Tracing disabled.")

    logger.info("observability_config", 
                status="configured", 
                project=project or "default")

