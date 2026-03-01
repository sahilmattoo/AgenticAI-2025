# Demo: LangChain Tool-Using Agent with Performance Monitoring

## Introduction
This demo showcases how to create a **LangChain agent** equipped with multiple tools — such as **Wikipedia search** and **a calculator** — and monitor its **response latency**, **token usage**, and **cost metrics**.

It demonstrates a practical deployment scenario from *Week 16: Observability and Monitoring of Deployed Agentic Systems.*

The agent uses:
- **LangGraph** for workflow orchestration  
- **Evidently AI** for drift and performance analysis  
- **LangSmith** for tracing and observability

---

## 1. Environment Setup

### Step 1 – Create a new virtual environment
Create an isolated environment for this demo.

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

---

## 2. Setting Up LangSmith Account and API Key

1. Go to **[LangSmith](https://smith.langchain.com)** and sign in using your GitHub or Google account.  
2. Navigate to **Settings → API Keys**.  
3. Click **Create API Key**, name it (for example `Agent_Performance_Monitoring`), and copy the generated key.  
4. Open your project’s `config/settings.py` file and update the following section:

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Agent_Performance_Monitoring"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "your_langsmith_api_key_here"
```

Make sure the key value is enclosed in quotes and not shared publicly.

---

## 3. Running the Demo

Once the environment and keys are configured, start the application:

```bash
python app.py
```

The program will:

1. Initialize OpenAI and LangSmith credentials from `config/settings.py`.  
2. Build a **LangGraph-based agent** capable of using tools like Wikipedia search and calculator.  
3. Execute two agent runs: a normal reference run and a simulated slow run.  
4. Collect **latency** and **token usage** metrics for both runs.  
5. Generate an **Evidently drift report** comparing both executions.  
6. Save the report locally as `reports/drift_report.html`.

---

## 4. Viewing the Results

After execution:

- Open the generated report in your browser:
  ```
  reports/drift_report.html
  ```

  The report shows latency drift, token-count drift, and distribution statistics.

- LangSmith traces for each agent invocation are automatically recorded.

---

## 5. Accessing the LangSmith Dashboard

Open the official LangSmith dashboard in your browser:

**https://smith.langchain.com**

This is the central hub for viewing all your projects, traces, and runs.

In the **Agent_Performance_Monitoring** project, each new run appears as a trace entry with detailed insights:

- **Input:** “Calculate 12 × 15 using the calculator tool”  
- **Output:** “180”  
- **LLM Details:** model name, latency, and token usage  
- **Tool Calls:** shows calculator tool execution and result  
- **Execution Graph:** hierarchical view of LLM → Tool → Final Answer  

Each run can be inspected individually for:
- Performance analysis  
- Prompt debugging  
- Drift monitoring over time  

---

## 6. Summary

This modular demo integrates:
- **LangChain + LangGraph** → Agent workflow  
- **Evidently AI** → Performance and drift monitoring  
- **LangSmith** → Tracing and observability  

Together, these provide a foundation for **production-grade agent monitoring** and **traceable AI performance evaluation**.
