"""
Module: Metrics
Simulates slower agent runs for drift comparison.
"""

import time
import pandas as pd


from config.observability import get_request_id

def run_slow_agent(agent, query_list, session_id="slow-session", delay: float = 1.0):
    """Runs the agent with artificial delay."""
    results = []
    for q in query_list:
        request_id = get_request_id()
        start_time = time.time()
        time.sleep(delay)
        try:
            response = agent.invoke({
                "input": q, 
                "session_id": session_id, 
                "request_id": request_id,
                "history": []
            })
            output = response.get("output", response)
            path = response.get("path", "unknown")
        except Exception as e:
            output = f"Error: {str(e)}"
            path = "error"
            
        end_time = time.time()
        latency = end_time - start_time
        token_count = len(str(output).split())
        results.append({
            "query": q,
            "response": output,
            "latency": latency,
            "token_count": token_count,
            "path": path,
            "request_id": request_id
        })
    return pd.DataFrame(results)
