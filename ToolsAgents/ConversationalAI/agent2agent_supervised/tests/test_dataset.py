import pytest
from agent2agent_dataset import Agent2AgentDataset


def test_dataset_loads(tmp_path):
    p = tmp_path / "data.jsonl"
    p.write_text('{"input": "A: Hello\nB:", "target": "Hi"}\n')
    ds = Agent2AgentDataset(str(p))
    assert len(ds) == 1
    ex = ds[0]
    assert "input" in ex and "target" in ex
