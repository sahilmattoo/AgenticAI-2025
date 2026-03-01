"""
Routing logic to determine execution path.
Demonstrates separation of concerns between heuristic/logic rules and LLM calls.
"""
from .prompts import ROUTER_PROMPT

def route_request(query: str) -> str:
    """
    Determines the routing path for a given query.
    
    Args:
        query: User input string
        
    Returns:
        'rule' or 'agent'
    """
    query_lower = query.lower()
    
    # Hardcoded heuristics for stability & speed
    if any(keyword in query_lower for keyword in ["status", "uptime", "version", "ping"]):
        return "rule"
        
    # Default to agent for everything else
    # In a more complex system, this might use a lightweight classifier or LLM call
    return "agent"
