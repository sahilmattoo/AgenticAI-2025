
## Output Distribution Drift


from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

baseline_outputs = [
    "Clause 4 defines termination conditions.",
    "Payment terms are specified in section 7."
]

new_outputs = [
    "The contract ends when parties decide.",
    "Section 7 explains billing cycles."
]

def compute_centroid(texts):
    embeddings = model.encode(texts)
    return np.mean(embeddings, axis=0)

baseline_centroid = compute_centroid(baseline_outputs)
new_centroid = compute_centroid(new_outputs)

drift_score = np.linalg.norm(baseline_centroid - new_centroid)

print("Drift Score:", drift_score)



"""Tool Usage Pattern Drift"""

from collections import Counter

baseline_tool_usage = ["search", "search", "summarize"]
new_tool_usage = ["search", "search", "search", "summarize"]

baseline_count = Counter(baseline_tool_usage)
new_count = Counter(new_tool_usage)

print("Tool Usage Drift:", new_count["search"] - baseline_count["search"])


## Reasoning Pattern Drift (Advanced)
"""
Track:

Chain-of-thought length

Step count in LangGraph

State transitions
"""

baseline_avg_steps = 4.2
current_avg_steps = 7.9

if current_avg_steps > baseline_avg_steps * 1.5:
    print("⚠ Agent Over-Reasoning Drift")
    
