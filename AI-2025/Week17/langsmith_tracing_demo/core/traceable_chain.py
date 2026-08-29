"""
Defines a traceable chain that logs all interactions in LangSmith.
"""

from langsmith import traceable
from core.model import llm
from core.prompt import prompt

@traceable(run_type="chain")
def ask_agent(question: str):
    """Executes a LangChain | LangSmith traced agent query."""
    chain = prompt | llm
    result = chain.invoke({"question": question})
    return result.content
