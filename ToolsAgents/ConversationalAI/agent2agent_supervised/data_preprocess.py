import json
from pathlib import Path

# Small helper to convert a CSV or logs into the expected JSONL format.
# For demonstration we include a tiny example transformation.

def make_jsonl(output_path: str):
    examples = [
        {"input": "AgentA: Hi, what's your status?\nAgentB:", "target": "I'm in progress, ETA 2 hours."},
        {"input": "AgentA: Can you prioritize task X?\nAgentB:", "target": "Yes, I'll move task X to today."},
        {"input": "AgentA: Did you finish the review?\nAgentB:", "target": "Review completed, comments added."}
    ]
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        for ex in examples:
            fh.write(json.dumps(ex, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    make_jsonl("./agent2agent_supervised/sample_data.jsonl")
