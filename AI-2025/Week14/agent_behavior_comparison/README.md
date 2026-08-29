# Agent Behavior Comparison System

## Introduction
This project serves as a hands-on demonstration comparing two architectural paradigms in AI agent design:
1. Static, Rule-Based Routing (Representative of early "Week 9" systems)
2. Policy-Driven Adaptive Routing (Advanced "Week 14" systems)

## Purpose of the Demo
The goal is to visibly demonstrate why static agents fail in dynamic production environments and how adaptive policy layers enable resilience and evolution without code changes.

## What This System Is
- A side-by-side comparison of deterministic vs. probabilistic control.
- A demonstration of explicit policy objects governing agent behavior.
- A showcase of LangSmith for observability and debugging in adaptive systems.

## What This System Is NOT
- A basic LangChain tutorial.
- A "Hello World" chat bot.
- A demonstration of model training, fine-tuning, or reinforcement learning.

## Comparison: Static vs. Adaptive

### Static Mode
- **Logic**: Keyword matching (e.g., if "payment" in query -> Routing: BILLING).
- **State**: None. Every run is identical.
- **Feedback**: Ignored. The system cannot learn from mistakes.
- **Observability**: Minimal console logs. No tracing.

### Adaptive Mode
- **Logic**: LLM-based decision making guided by an explicit Policy Object.
- **State**: Persistent `data/policy_history.json`.
- **Feedback**: Active. User feedback passes through an Evaluator to update the Policy.
- **Observability**: Full LangSmith integration (Inputs, Outputs, Latency, Policy Versions).

## How LangSmith is Used
LangSmith is enabled ONLY in Adaptive Mode. It captures the decision trace including:
- The input query.
- The active policy version.
- The agent's reasoning.
- The result of any feedback evaluation.

This allows engineers to inspect *why* a routing decision changed over time as the policy evolved.

## Evolution in Production
In a real-world system, this "Policy Engine" allows product teams to tune agent behavior (e.g., "Be more cautious with billing queries") without requiring engineering teams to deploy new code. The feedback loop acts as a governance layer.
