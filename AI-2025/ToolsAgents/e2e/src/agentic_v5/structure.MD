agentic_hr_ai/
│
├── documents/
│      onboarding.pdf
│      code_of_conduct.pdf
│
├── src/
│
│   ├── ingest.py
│   │      Build FAISS index
│
│   ├── tools.py
│   │      HR retrieval tool
│   │      Ethics violation detector
│
│   ├── evaluator_tools.py
│   │      relevance_checker
│   │      policy_alignment_checker
│   │      ethics_tone_checker
│
│   ├── evaluator_agent.py
│   │      Evaluation agent (LLM-as-Judge)
│
│   ├── hr_agent.py
│   │      Main HR assistant agent
│
│   └── run_agent.py
│          Entry point for running the system