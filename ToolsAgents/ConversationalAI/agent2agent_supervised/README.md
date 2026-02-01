# Agent2Agent Supervised Template

This folder contains a minimal supervised learning template to fine-tune a seq2seq model for Agent-to-Agent response generation.

Quick start:

1. Create a virtualenv and install dependencies:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Generate sample data:

```
python data_preprocess.py
```

3. Train a small model locally:

```
python train.py --data sample_data.jsonl --model t5-small --output_dir ./out --epochs 1 --batch_size 2
```

4. Evaluate:

```
python evaluate.py ./out sample_data.jsonl
```

Files:
- `agent2agent_dataset.py`: small reader for JSONL input/target pairs
- `agent2agent_model.py`: helper to load model + tokenizer
- `train.py`: training script using Hugging Face Trainer
- `evaluate.py`: simple generation-based evaluator
- `data_preprocess.py`: example data creation
- `sample_data.jsonl`: tiny sample dataset
- `requirements.txt`: dependencies
- `tests/test_dataset.py`: minimal unit test (see tests folder)
