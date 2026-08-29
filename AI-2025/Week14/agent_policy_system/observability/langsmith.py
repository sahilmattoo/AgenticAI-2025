import os
from langchain_core.tracers.context import tracing_v2_enabled

def validate_tracing_config():
    """
    Checks if necessary environment variables for LangSmith are set.
    """
    required_vars = ["LANGCHAIN_API_KEY", "LANGCHAIN_TRACING_V2"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"WARNING: LangSmith tracing is NOT fully configured. Missing: {', '.join(missing)}")
        print("Tracing will likely strictly local or disabled.")
    else:
        print("LangSmith tracing is ENABLED.")

def get_trace_context(run_name: str, tags: list = None, metadata: dict = None):
    """
    Returns a context manager for tracing with specific tags and metadata.
    """
    return tracing_v2_enabled(project_name=os.getenv("LANGCHAIN_PROJECT", "default"), tags=tags)
