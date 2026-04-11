# 📊 Agentic AI Capstone — Evaluation Criteria

## 🎯 Purpose

This document defines how the AI Agent will be evaluated based on:

- Reliability (Trust)
- Safety (Guardrails)
- Explainability
- Engineering Design
- Practical Usefulness

---

# 🧠 1. Core Evaluation Dimensions

## ✅ 1. Reliability (Trust)

**Definition:**  
The agent provides accurate, consistent, and grounded responses.

### Evaluation Metrics:
- Accuracy of responses (>90%)
- Consistency across similar queries
- Grounded responses (based on RAG / data)
- Minimal hallucination

### Evidence Required:
- Before vs After (with/without RAG)
- Sample logs of correct responses

---

## 🔐 2. Safety-First Behaviour (Guardrails)

**Definition:**  
The agent prevents unsafe, illegal, or restricted actions.

### Requirements:
- Must refuse transactional or unsafe requests
- Must not execute actions
- Must escalate risky scenarios
- Must not store sensitive data in logs

### Evaluation Metrics:
- 100% refusal of unsafe queries
- Correct escalation handling
- No PII leakage

### Evidence Required:
- Refusal examples
- Escalation examples
- Masked logs

---

## 🔍 3. Explainability

**Definition:**  
The agent explains *why* it gave a response.

### Evaluation Metrics:
- Uses retrieved context (RAG)
- References policies/data
- Provides reasoning clarity

### Evidence Required:
- Responses with context
- Source-backed answers

---

## ⚙️ 4. Engineering Design Quality

**Definition:**  
Quality of system architecture and decision-making.

### Evaluation Criteria:
- Proper use of:
  - RAG
  - Tools
  - Memory
  - Guardrails
- Clear modular design
- Justified architectural decisions

### Evidence Required:
- Architecture diagram
- Design justification document

---

## 🔁 5. Agent Capabilities (Phase-wise Evaluation)

### Phase 1: Problem Framing
- Clear user persona
- Defined workflow
- Success criteria
- Edge cases identified

---

### Phase 2: Baseline Agent
- Simple rule-based agent
- Demonstrated limitations

---

### Phase 3: LLM Integration
- Improved responses
- Prompt comparison (2–3 variants)

---

### Phase 4: Retrieval (RAG)
- Document-based answering
- Improvement over baseline

---

### Phase 5: Tool Usage
- At least 2 tools implemented
- Correct tool selection
- Demonstration of failed tool call

---

### Phase 6: Memory & Context
- Multi-turn conversation support
- Context retention

---

### Phase 7: Adaptive Behaviour
- Feedback-based improvement
- Before vs after comparison

---

### Phase 8: Deployment Readiness
- Logging and tracing
- Error handling
- Latency tracking

---

### Phase 9: Evaluation & Review
- Test scenarios created
- Failure analysis
- Root cause + fix
- Improvement roadmap

---

# 📊 6. Evaluation Metrics Summary

| Category | Metric | Target |
|--------|--------|--------|
| Accuracy | Correct responses | > 90% |
| Safety | Unsafe request refusal | 100% |
| Grounding | RAG-based answers | > 90% |
| Tool Usage | Correct tool calls | > 90% |
| Escalation | Correct escalation | > 95% |
| Latency | Response time | < 3 sec |

---

# ⚠️ 7. Failure Cases & Risk Handling

## Common Risks:

### ❌ Hallucination
- **Cause:** No grounding
- **Mitigation:** RAG + strict prompt

---

### ❌ Unsafe Actions
- **Cause:** Missing guardrails
- **Mitigation:** Refusal logic

---

### ❌ Ambiguity
- **Cause:** Incomplete query
- **Mitigation:** Clarification prompts

---

### ❌ Tool Failure
- **Cause:** API errors
- **Mitigation:** Graceful fallback

---

### ❌ Context Loss
- **Cause:** No memory
- **Mitigation:** Session memory

---

# 🧠 8. Design Justification

The agent design must justify:

- Why RAG is used (accuracy, grounding)
- Why tools are used (real capability)
- Why guardrails are needed (safety)
- Why memory is required (context)
- Why adaptive logic is added (better UX)

---

# 🧪 9. Live Demo Evaluation

During evaluation:

- Testers will provide random queries
- System must demonstrate:
  - Correct answers
  - Safe refusals
  - Proper escalation
  - Tool usage
  - Context awareness

---

# 🚀 Final Summary

> The agent will be evaluated on its ability to provide reliable, explainable, and safe responses while demonstrating real-world usefulness through retrieval, tool usage, memory, and adaptive behavior.

---