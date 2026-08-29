import os
from langchain_core.tracers.context import tracing_v2_enabled

def validate_tracing():
    """
    Checks if tracing is active.
    """
    if os.getenv("LANGCHAIN_TRACING_V2") == "true" and os.getenv("LANGCHAIN_API_KEY"):
        return True
    return False

def get_trace_context(run_name: str, tags: list = None):
    """
    Returns a context manager for matching the previous project's style.
    """
    return tracing_v2_enabled(project_name=os.getenv("LANGCHAIN_PROJECT", "agent-comparison"), tags=tags)
