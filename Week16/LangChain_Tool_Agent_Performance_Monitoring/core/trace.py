"""
Module: Trace
Integrates LangSmith tracing for performance monitoring.
Relies on environment variables defined in config/settings.py.
"""

from langsmith import Client, traceable
from config import settings  # ensures env vars (OpenAI + LangSmith) are loaded


def init_langsmith():
    """Initialize LangSmith client using environment variables."""
    try:
        client = Client()

        # Handle generator-based API response safely
        projects = list(client.list_projects())
        project_name = projects[0].name if projects else settings.os.environ.get("LANGCHAIN_PROJECT", "Agent_Performance_Monitoring")

        print(f"[OK] Connected to LangSmith project: {project_name}")
        return client

    except Exception as e:
        print(f"[WARNING] LangSmith initialization failed: {e}")
        print("Check your API key or internet connection.")
        return None


@traceable(run_type="chain")
def run_agent_with_trace(agent, query: str, session_id: str = "trace-session"):
    """Execute one traced agent call."""
    from config.observability import get_request_id
    request_id = get_request_id()
    
    result = agent.invoke({
        "input": query, 
        "session_id": session_id, 
        "request_id": request_id,
        "history": []
    })
    
    if isinstance(result, dict) and "output" in result:
        return result["output"]
    return result
