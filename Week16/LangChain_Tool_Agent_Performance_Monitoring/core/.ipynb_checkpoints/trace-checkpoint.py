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

        print(f"✅ Connected to LangSmith project: {project_name}")
        return client

    except Exception as e:
        print(f"⚠️ LangSmith initialization failed: {e}")
        print("Check your API key or internet connection.")
        return None


@traceable(run_type="chain")
def run_agent_with_trace(agent, query: str):
    """Execute one traced agent call."""
    result = agent.invoke({"input": query})
    if isinstance(result, dict) and "output" in result:
        return result["output"]
    return result
