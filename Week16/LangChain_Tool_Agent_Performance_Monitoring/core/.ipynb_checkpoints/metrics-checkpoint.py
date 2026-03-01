"""
Module: Metrics
Simulates slower agent runs for drift comparison.
"""

import time
import pandas as pd


def run_slow_agent(agent, query_list, delay: float = 1.0):
    """Runs the agent with artificial delay."""
    results = []
    for q in query_list:
        start_time = time.time()
        time.sleep(delay)
        try:
            response = agent.invoke({"input": q})
            output = response.get("output", response)
        except Exception as e:
            output = str(e)
        end_time = time.time()
        latency = end_time - start_time
        token_count = len(str(output).split())
        results.append({
            "query": q,
            "response": output,
            "latency": latency,
            "token_count": token_count
        })
    return pd.DataFrame(results)
