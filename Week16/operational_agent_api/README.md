# Operational Agent API

## Overview
This system is a reference implementation of a production-ready Agent API. It demonstrates the operational requirements for deploying, monitoring, and evaluating agentic systems.

**Note:** This is an educational demo for Week 16 of the Advanced Agentic AI course. It focuses on the post-deployment lifecycle rather than the agent construction itself.

## Purpose
The primary goal is to illustrate:
1.  **Runtime Behavior:** How agents behave under real traffic.
2.  **Observability:** The necessity of structured logging and tracing (via LangSmith).
3.  **Evaluation:** The importance of separating logic evaluation from deployment.
4.  **Reliability:** How to detect silent failures in probabilistic systems.

## System Architecture

### Components
*   **API Layer:** FastAPI service handling request lifecycle, ID generation, and middleware logging.
*   **Routing Logic:** Deterministic heuristics to offload simple queries from the LLM.
*   **Agent Core:** LangChain-based agent for complex reasoning tasks.
*   **Memory Store:** In-memory session state management (mocking a Redis/Memcached layer).
*   **Observability:**
    *   **Structured Logging:** JSON-formatted logs for latency, routing decisions, and errors.
    *   **LangSmith:** Deep tracing for chain execution and prompt management.

### Directory Structure
*   `app/core`: Core business logic (Agent, Router, Memory).
*   `app/observability`: Logging and Tracing configurations.
*   `app/evaluation`: Independent evaluation logic.
*   `tests/`: Integration and regression tests.

## Observability Strategy

### Structured Logging
All logs are emitted in JSON format to facilitate ingestion by log aggregation systems (e.g., Datadog, ELK). Key fields include:
*   `request_id`: Unique trace ID for the HTTP request.
*   `session_id`: User session identifier.
*   `latency_ms`: Execution time in milliseconds.
*   `route`: The path taken (rule vs. agent).

### LangSmith Integration
LangSmith is used for:
1.  **Debugging:** Inspecting full traces of failed agent interactions.
2.  **Governance:** Monitoring token usage and prompt versions.
3.  **Evaluation:** Comparing production traces against baseline datasets.

## Setup and Usage

### Prerequisites
*   Python 3.10+
*   OpenAI API Key
*   LangChain API Key (for LangSmith)

### Installation
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
1.  Create a `.env` file in the root directory (or use the one provided) with your credentials:
    ```env
    OPENAI_API_KEY=sk-...
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_PROJECT=adaptive-agent-demo
    LANGCHAIN_API_KEY=lsv2-...
    ```

### Running the Service
Start the API server:
```bash
uvicorn app.main:app --reload
```
The service will be available at `http://localhost:8000`.

### Verifying Operation (What Next?)
Once the server is running, you can verify it is working correctly by running the included demo client script:

```bash
python demo_client.py
```
This script will:
1.  Ping the `/health` endpoint.
2.  Send a rule-based query (e.g., status check) to verify fast-path routing.
3.  Send a complex query to the Agent to verify the LLM integration and 
    observability pipeline.

### Running Tests
Execute the verification suite:
```bash
python -m pytest tests/
```
This runs both smoke tests (API connectivity) and evaluation tests (logic correctness).

## Evaluation
The system includes a standalone evaluation suite in `app/evaluation`. This allows for regression testing of the agent's logic without requiring a full deployment.

To run specific evaluation checks:
```bash
pytest tests/evaluation_tests.py
```

## Disclaimer
This project is not intended to be a tutorial on building agents. It assumes the agent logic exists and focuses exclusively on the operational wrapper required for a reliable production deployment.
