# Demo: LangSmith Tracing with LangChain

## Introduction
This demo illustrates how to integrate **LangSmith tracing** into a **LangChain agent**, enabling detailed observability of model reasoning, latency, token usage, and tool interactions.

The workflow creates a **traceable chain** using the LangSmith client and LangChain’s modular components (`ChatPromptTemplate`, `ChatOpenAI`, and `traceable` decorator).  

This is a lightweight demonstration of how **agent telemetry** can be captured and analyzed via the LangSmith dashboard — forming the foundation of **LLMOps monitoring** and **AI system observability**.

---

## 1. Environment Setup

### Step 1 – Create a new virtual environment
To keep dependencies isolated and reproducible, create a new environment.

#### Windows PowerShell
```bash
python -m venv lcenv
```

#### macOS / Linux (Bash)
```bash
python3 -m venv lcenv
```

---

### Step 2 – Activate the environment

#### Windows PowerShell
```bash
.\lcenv\Scriptsctivate
```

#### macOS / Linux (Bash)
```bash
source lcenv/bin/activate
```

---

### Step 3 – Install dependencies
All required libraries are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain:
```text
langchain==0.3.9
langchain-openai==0.2.11
langsmith==0.1.147
```

---

## 2. Setting Up LangSmith Account and API Key

To enable tracing and observability, LangSmith credentials must be configured.

### Step 1 – Create your LangSmith Account
Visit **[LangSmith](https://smith.langchain.com)** and sign up using your Google or GitHub account.

### Step 2 – Generate API Key
1. Go to **Settings → API Keys**  
2. Click **Create API Key**  
3. Name it (e.g., `LangSmith_Tracing_Demo`)  
4. Copy the key safely  

### Step 3 – Configure Environment Variables
Open your project’s `config/settings.py` and add the following:

```python
import os

# --- API and Project Configuration ---
os.environ["OPENAI_API_KEY"] = "your_openai_key_here"
os.environ["LANGCHAIN_API_KEY"] = "your_langsmith_api_key_here"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangSmith_Tracing_Demo"

print("✅ Environment variables loaded successfully.")
```

This ensures the LangSmith client is initialized automatically when the project runs.

---

## 3. Project Structure

Your modular project layout should look like this:

```
langsmith_tracing_demo/
│
├── app.py                    # Main entry point to run demo queries
│
├── core/
│   ├── model.py              # Initializes ChatOpenAI model
│   ├── prompt.py             # Defines ChatPromptTemplate
│   ├── traceable_chain.py    # Contains @traceable agent logic
│   └── __init__.py
│
├── config/
│   └── settings.py           # Environment variables setup
│
├── tests/
│   └── smoke_test.py         # Optional file for quick verification
│
├── requirements.txt
└── README.md
```

---

## 4. How the Demo Works

### Step 1 – Load Configuration
The system loads OpenAI and LangSmith credentials from `config/settings.py`.

### Step 2 – Initialize Model and Prompt
`ChatOpenAI` is used as the model, and `ChatPromptTemplate` formats concise assistant responses.

```python
"You are a helpful assistant. Answer concisely.\n\nQuestion: {question}"
```

### Step 3 – Create Traceable Function
The `@traceable(run_type="chain")` decorator logs every agent run in the LangSmith dashboard, capturing:
- Input and output  
- Execution time and cost  
- Token usage  
- Full reasoning chain

### Step 4 – Run Queries
The `app.py` executes multiple test queries and prints both the queries and responses to the console.

---

## 5. Running the Demo

Once the environment is ready and credentials are set:

```bash
python app.py
```

Expected console output:

```
Query: Who discovered penicillin?
Answer: Alexander Fleming
--------------------------------------------------------------------------------
Query: Explain the difference between AI and machine learning.
Answer: AI is the broader field; ML is a subset using data to learn patterns.
--------------------------------------------------------------------------------
Query: What is the square root of 256?
Answer: 16
--------------------------------------------------------------------------------
```

Each query execution is automatically traced in LangSmith under the project `LangSmith_Tracing_Demo`.

---

## 6. Accessing the LangSmith Dashboard

Open the official LangSmith dashboard in your browser:

**https://smith.langchain.com**

That’s the central hub for viewing all your **projects**, **traces**, and **runs**.

In your **LangSmith_Tracing_Demo** project, you will see detailed trace entries for every execution.

### Each trace includes:
- **Input:** “Calculate 12 × 15 using the calculator tool”  
- **Output:** “180”  
- **LLM Details:** model name, latency, and token usage  
- **Execution Graph:** hierarchical view of LLM → Output chain  
- **Metadata:** time, version, and cost per query  

You can drill into each run to visualize:
- Model reasoning  
- Prompt and completion tokens  
- Latency metrics  
- Reproducibility and debug traces

---

## 7. Reflection and Applications

This demo demonstrates how LangSmith can be integrated to:
- Track every inference and prompt change  
- Debug and visualize LLM reasoning paths  
- Measure latency and usage metrics for optimization  
- Enable full observability in production AI agents  

This architecture can easily scale to support:
- **RAG pipelines**
- **Tool-based agents**
- **Multi-step workflows**
- **Continuous performance monitoring**

---

## 8. Summary

This modular demo integrates:
- **LangChain** → LLM orchestration  
- **LangSmith** → Tracing and monitoring  
- **Python modularization** → Reproducibility and clarity  

Together, these provide a foundation for **transparent, monitored AI development**, ensuring all LLM interactions are observable, testable, and production-ready.

---

## 9. Next Steps

- Add **Evidently AI** for data drift tracking.  
- Log **cost and latency metrics** over time.  
- Extend tracing to multi-agent workflows.  
- Integrate **OpenTelemetry** for unified monitoring pipelines.  
---
