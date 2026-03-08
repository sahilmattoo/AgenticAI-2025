# Industry-Grade IT Support Agent (FastAPI)

## Introduction
This project demonstrates an **end-to-end agentic workflow** for an IT Support Agent. It pivots from a simple debug demo to a professional-grade application using **FastAPI** for API management and **Structured JSON Logging** for observability.

The agent is designed to handle common IT infrastructure tasks:
- **Service Status Monitoring**: Checking availability of critical services (Payment, Shipping, etc.).
- **Log Analysis**: Investigating technical failures through automated log inspection.
- **Escalation Management**: Creating support tickets for unresolved or high-priority issues.

---

## 1. Project Architecture

The system follows a modular design:
- `main.py`: FastAPI entry point with `/predict` and health check (`/`) routes.
- `core/agent.py`: Agent logic for intent recognition and tool orchestration.
- `core/tools.py`: Specialized industrial tools for system interaction.
- `core/logger.py`: JSON-based structured logging for production observability.

---

## 2. Environment Setup

### Step 1 – Create virtual environment
```bash
python -m venv agentenv
```

### Step 2 – Activate the environment
```bash
. gentenv\Scripts ctivate  # Windows
source agentenv/bin/activate  # macOS / Linux
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

---

## 3. Running the API

Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

---

## 4. End-to-End Flow (Hands-on Examples)

### Example 1: Infrastructure Monitoring
**Scenario**: A user reports that the shipping service is having issues.
**Action**: The agent checks the status and retrieves relevant logs.

**Query**:
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"query": "The shipping service is down, can you check the logs?"}'
```

**Response**:
```json
{
  "query": "The shipping service is down, can you check the logs?",
  "response": "I analyzed the logs for the shipping service:\nLogs for shipping:\n2025-12-22 08:05:22 | CRITICAL | 503 Service Unavailable\n2025-12-22 08:06:45 | ERROR | Dependency 'PartnerAPI' unreachable",
  "status": "success"
}
```

### Example 2: Escalation Management
**Scenario**: An issue is critical and needs immediate human attention.
**Action**: The agent creates a support ticket with high priority.

**Query**:
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"query": "Urgent: Payment database connection failing. Please escalate."}'
```

**Response**:
```json
{
  "query": "Urgent: Payment database connection failing. Please escalate.",
  "response": "I've escalated this issue. Ticket TIC-4821 created successfully. Priority: High. Description: Urgent: Payment database connection failing. Please escalate..",
  "status": "success"
}
```

---

## 5. Industry Use Cases & Suggestions
To extend this project for other domains, consider the following:

- **Automated DevOps Support**: 
  - *Tool*: GitHub/GitLab integration to check PR status or CI/CD pipelines.
  - *Scenario*: "Check why the latest build for the 'frontend' branch failed."
- **Customer Success Agent**:
  - *Tool*: CRM integration (e.g., Salesforce) to retrieve customer history or billing status.
  - *Scenario*: "What is the subscription status for Customer #12345?"
- **Security Operations (SecOps)**:
  - *Tool*: Integration with SIEM tools to check for recent unauthorized login attempts.
  - *Scenario*: "Show me recent failed login attempts from IP 192.168.1.50."

---

## 6. Observability
Every interaction is logged in `logs/simple_agent_debug.log` in **Structured JSON format**. This is critical for:
- Traceability across multiple tool calls.
- Measuring latency for performance optimization.
- Analyzing failure patterns for model fine-tuning.
