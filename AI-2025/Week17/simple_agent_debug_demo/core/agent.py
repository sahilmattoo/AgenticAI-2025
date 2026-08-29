"""
Core logic for the IT Support Agent.
"""

import time
from core.logger import log_to_file
from core.tools import check_service_status, analyze_logs, create_support_ticket

def simple_agent(query: str) -> str:
    """Agent that handles IT support queries using specialized tools."""
    log_to_file(f"Received support query: {query}")
    start = time.time()
    query_lower = query.lower()
    
    try:
        # Step 1: Intent Recognition & Tool Selection
        if "status" in query_lower or "check" in query_lower:
            # Extract service name (simplified)
            service = "shipping" if "shipping" in query_lower else "payment"
            log_to_file(f"Agent Reasoning: Request to check status for {service}", tool_name="check_service_status")
            result = check_service_status(service)
            answer = f"I've checked the systems. {result}."
            
        elif "log" in query_lower or "failing" in query_lower:
            service = "shipping" if "shipping" in query_lower else "payment"
            log_to_file(f"Agent Reasoning: Investigating failures via logs for {service}", tool_name="analyze_logs")
            result = analyze_logs(service)
            answer = f"I analyzed the logs for the {service} service:\n{result}"
            
        elif "ticket" in query_lower or "escalate" in query_lower:
            log_to_file("Agent Reasoning: Creating a support ticket for escalation", tool_name="create_support_ticket")
            result = create_support_ticket(query, priority="High")
            answer = f"I've escalated this issue. {result}."
            
        else:
            log_to_file("Agent Reasoning: No specific IT tool identified. Providing general assistance.")
            answer = "I'm your IT Support Agent. I can check service status, analyze logs, or create support tickets. How can I help you today?"

    except Exception as e:
        log_to_file(f"Agent Failure: {str(e)}", error=True)
        answer = f"Agent failed due to: {str(e)}"

    finally:
        elapsed = time.time() - start
        log_to_file(f"Query processed", latency=f"{elapsed:.2f}s")

    return answer
