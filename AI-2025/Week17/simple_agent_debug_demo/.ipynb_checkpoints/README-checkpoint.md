# Demo: Debugging a Broken Agent

## Introduction
This demo simulates a **simple AI agent** that occasionally fails — either by using a non-existent tool or by parsing input incorrectly.  
The goal is to illustrate **debugging, logging, and traceability** concepts for agentic systems.

After each run, the application logs the agent’s reasoning steps, tools used, and errors into a local file:  
```
logs/simple_agent_debug.log
```

You can inspect this file to trace what caused the agent to fail and how it handled different inputs.

---

## 1. Environment Setup

### Step 1 – Create virtual environment
```bash
python -m venv agentenv
```

### Step 2 – Activate the environment

**Windows PowerShell**
```bash
.gentenv\Scriptsctivate
```

**macOS / Linux**
```bash
source agentenv/bin/activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

---

## 2. Running the Demo
```bash
python app.py
```

Once launched, a **Gradio interface** will open in your browser.  
Enter test inputs such as:
```
calc 45 6
calc 78*7
hello there
```

You’ll observe that sometimes the agent returns the correct answer, while other times it throws an error like:
```
Agent failed due to: Tool 'BrokenCalculator' not found
```

This randomness is intentional — it mimics **real-world agent failures** for debugging practice.

---

## 3. Understanding Logs
All interactions are stored in:
```
logs/simple_agent_debug.log
```

Each log line includes:
```
YYYY-MM-DD HH:MM:SS | INFO/ERROR | Message
```

Example:
```
2025-11-10 19:45:02 | INFO | Trying to use tool: BrokenCalculator
2025-11-10 19:45:02 | ERROR | Error occurred: Tool 'BrokenCalculator' not found
2025-11-10 19:45:02 | INFO | Query completed in 0.04s
```

This structured log format helps in:
- Tracking tool usage  
- Measuring response latency  
- Identifying recurring failure patterns  

---

## 4. How It Works

1. **simple_agent()** processes queries, simulating occasional tool failures.  
2. **log_to_file()** immediately writes to a log file (no buffering).  
3. **Gradio UI** provides an interactive test interface.  
4. The randomness allows repeated experiments to observe different failure paths.

---

## 5. Real-World Extension Ideas
You can extend this example by:
- Integrating **LangSmith tracing** for visualization  
- Adding **OpenTelemetry** for distributed monitoring  
- Using **Evidently AI** to track behavioral drift  
- Displaying logs directly in Gradio UI  

---

## 6. Summary
This demo provides a minimal reproducible scenario for debugging and monitoring AI agents.
It introduces concepts of **logging, fault tracing, and runtime observability** in a safe sandboxed way — perfect for introductory observability training.

---

## 7. Expected Outcome
After running several inputs, open:
```
logs/simple_agent_debug.log
```
You’ll find:
- Successful runs (correct tool usage)
- Failures due to broken tools
- Execution time for each query

This log serves as your **primary debugging artifact**, much like trace logs in production systems.
