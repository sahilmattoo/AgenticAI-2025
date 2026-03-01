# Operational Monitoring of Tool-Using Agents: Latency, Cost, and Drift

## Position Statement
This demo does not teach how to build a tool-using agent.
It teaches how to detect, explain, and diagnose performance drift in deployed agentic systems.

## Overview
This system demonstrates a production scenario where a deployed tool-using agent begins to exhibit performance degradation. In Week 16, we move beyond "does it work?" to "is it working well over time?".

We use **LangSmith** for trace-level root cause analysis and **Evidently** for aggregate drift detection.

## System Description
The system consists of a pre-deployed LangGraph agent compliant with the Agentic Design Patterns from Week 14. 

- **Components**:
  - `core/agent.py`: A routing agent capable of using search and calculator tools.
  - `core/metrics.py`: Simulation logic to inject latency and verbosity (emulating "drift").
  - `core/report.py`: Evidently AI pipeline for statistical distribution checks.

- **Tools**:
  - `tool_wikipedia`: External knowledge retrieval.
  - `tool_calculator`: Mathematical computation.

## Operational Flow

### 1. Baseline Execution
The system executes a batch of canonical queries against the standard agent configuration. 
- **Metrics Captured**: Latency (ms), Token Usage, Tool Call Frequency.
- **Trace Destination**: LangSmith Project `Agent_Performance_Monitoring`.

### 2. Degraded Execution (Simulated)
The system executes the same query batch against a "drifted" version of the agent. This simulates common production issues:
- API latency improvements/regressions.
- Model updates leading to more verbose reasoning (token drift).
- Network overhead.

### 3. Drift Analysis (Evidently)
We compare the Baseline and Degraded distributions to generate a `drift_report.html`. This report highlights:
- **Latency Drift**: Statistical shifts in response time distribution (Wasserstein distance).
- **Token Drift**: Changes in consumption impacting cost.

### 4. Diagnosis (LangSmith)
Operators use LangSmith to inspect specific high-latency traces identified in the report. The analysis focuses on:
- "Why did this specific query take 2x longer?"
- "Did the agent take a different routing path?"
- "Is the tool call itself slower, or is the LLM generating more tokens?"

## Running the Monitoring Pipeline
Ensure your environment is configured with `OPENAI_API_KEY` and LangSmith credentials in `.env`.

```bash
python app.py
```

## Output Artifacts
- **Trace Data**: Viewable in the LangSmith Dashboard.
- **Drift Report**: Generated at `reports/drift_report.html`. 

## Why This Matters
In production, agents are probabilistic software. Unlike deterministic services, they can "fail" by becoming 30% more expensive or 50% slower without throwing a single exception. 

This reference architecture provides the observability stack required to catch these silent failures.
