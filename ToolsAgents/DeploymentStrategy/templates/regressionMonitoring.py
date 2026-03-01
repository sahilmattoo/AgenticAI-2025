from datetime import datetime
import pandas as pd

TEST_QUERIES = [
    "Who founded SpaceX?",
    "Calculate 23 * 17",
    "When was the first iPhone released?"
]

def monitor_token_drift(agent):
    results = []

    for q in TEST_QUERIES:
        response = agent.invoke({"input": q})
        tokens = len(str(response["output"]).split())

        results.append({
            "query": q,
            "tokens": tokens,
            "timestamp": datetime.now()
        })

    return pd.DataFrame(results)