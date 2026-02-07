# Agentic AI Policy Adaptation System (Week 14 Demo)

## Overview
This system is an advanced, production-oriented demonstration of **Policy-Driven Agent Adaptation**. 
Unlike "Hello World" tutorials that hardcode behavior, this project builds a closed-loop system where an agent constantly evolves its behavior based on user feedback—without requiring model fine-tuning or retraining.

### The Problem it Solves
In production, users often want agents to change *how* they respond (e.g., "be shorter," "be more formal") without changing the underlying code or prompt templates manually. This system automates that "tuning" process.

## Architecture & Workflow

The system operates on a cyclic **Run $\rightarrow$ Feedback $\rightarrow$ Update $\rightarrow$ Run** loop:

1.  **Task Execution (Run 1)**: 
    - The **Agent** receives a user task.
    - It consults the **Policy Engine** for the current `ResponsePolicy` (e.g., `verbosity=medium`).
    - It generates a response.
2.  **Feedback Collection**: 
    - The user provides natural language feedback (e.g., *"This is too wordy, just give me the facts"*).
3.  **Evaluation (The "Brain")**:
    - The **Evaluator** (an LLM-as-a-Judge) analyzes the feedback.
    - It maps the vague user complaint into a structured **Policy Delta** (e.g., `{"verbosity": "short"}`).
    - *Note: This ensures deterministic updates from unstructured input.*
4.  **Policy Update**:
    - The **Policy Engine** applies the delta to the current state.
    - The new policy is persisted in `data/policy_history.json`.
5.  **Adapted Execution (Run 2)**:
    - The **Agent** re-runs the task with the *new* policy.
    - The difference in output demonstrates immediate adaptation.

##  Core Components

| Component | File | Role |
| :--- | :--- | :--- |
| **ResponsePolicy** | `core/policy_engine.py` | The "Configuration Object". It holds the state of *how* the agent should behave (Tone, Verbosity, Structure). |
| **PromptBuilder** | `core/prompts.py` | Dynamic Prompt Engineer. It takes a `ResponsePolicy` and generates the precise System Instruction for the LLM. |
| **Evaluator** | `core/evaluator.py` | The Feedback Processor. It uses a low-temperature LLM to translate human complaints into JSON configuration updates. |
| **Agent** | `core/agent.py` | The Worker. It simply executes tasks using the prompts given to it. |
| **LangSmith** | `observability/langsmith.py` | The Black Box Recorder. It logs every step so you can debug *why* a policy changed. |

## 📦 Observability (LangSmith)
This project is fully integrated with LangSmith. When you run the demo, check your [LangSmith Projects](https://smith.langchain.com) for `adaptive-agent-demo`.

You will see traces tagged with:
-   `policy_v1`: The behavior before feedback.
-   `evaluator`: The decision-making process of converting feedback to data.
-   `adapted` / `policy_v2`: The behavior after the update.

## How to Run

### 1. Prerequisites
- Python 3.10+
- OpenAI API Key

### 2. Setup
```bash
# Install dependencies
pip install -r agent_policy_system/requirements.txt

# Configure Environment
# Create a .env file in agent_policy_system/ with:
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=... (Optional, for tracing)
LANGCHAIN_TRACING_V2=true
```

### 3. Execution
Run the interactive CLI app:
```bash
python agent_policy_system/app.py
```

### 4. Interactive Steps
1.  **Enter a Task**: e.g., "Explain how a bicycle works."
2.  **Review Output**: See how the agent responds initially.
3.  **Give Feedback**: e.g., "Too informal, be more professional."
4.  **Observe Adaptation**: The system will analyze your feedback, update the internal policy, and reprint the answer in the new style.

## Key Takeaways for Production
-   **Policies vs. Prompts**: We don't change prompts directly; we update a *policy state*, which generates prompts. This is safer and more testable.
-   **Evaluator Reliability**: Using a separate LLM step to interpret feedback prevents "jailbreaks" and ensures valid configuration updates.
-   **Persistence**: Policies can be saved per-user or per-session (`data/policy_history.json`), creating a personalized experience over time.
