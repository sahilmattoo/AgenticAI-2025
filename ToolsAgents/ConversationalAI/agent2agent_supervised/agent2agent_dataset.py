from typing import List, Dict
import json
from pathlib import Path
from torch.utils.data import Dataset

class Agent2AgentDataset(Dataset):
    """Simple dataset for Agent-to-Agent supervised pairs.

    Expects a JSONL file with one JSON object per line: {"input": "...", "target": "..."}
    Tokenization is left to the trainer pipeline (we return raw strings).
    """

    def __init__(self, path: str):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Dataset file not found: {self.path}")

        self.examples = []
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                inp = obj.get("input")
                tgt = obj.get("target")
                if inp is None or tgt is None:
                    continue
                self.examples.append({"input": inp, "target": tgt})

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx) -> Dict[str, str]:
        return self.examples[idx]
