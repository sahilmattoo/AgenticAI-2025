"""
Main Application
Executes agent performance monitoring and drift analysis.
"""

from core.agent import create_agent, run_agent_with_metrics
from core.metrics import run_slow_agent
from core.report import generate_drift_report
from core.trace import init_langsmith, run_agent_with_trace

# --- Create and Compile Agent ---
agent = create_agent()

# --- Queries ---
queries = [
    "Who was the founder of SpaceX?",
    "Calculate 23 * 17",
    "When was the first iPhone released?",
    "Find population of France",
    "Calculate the area of a circle with radius 5"
]

# --- Run Agent ---
ref_metrics = run_agent_with_metrics(agent, queries)
cur_metrics = run_slow_agent(agent, queries)

print("\nReference Run Summary:\n", ref_metrics[["latency", "token_count"]].describe())
print("\nCurrent Run Summary:\n", cur_metrics[["latency", "token_count"]].describe())

# --- Generate Evidently Report ---
report = generate_drift_report(ref_metrics, cur_metrics)

# --- Show Reflection ---
print("""
Monitoring Completed!
- This report compares latency and token usage drift between two agent executions.
- Latency drift may reflect slower execution or network overhead.
- Token count drift may reflect verbosity differences from prompt or LLM updates.

Reflection Questions:
1. Which metric would you track in production for SLA compliance?
2. How might you log these metrics automatically using OpenTelemetry or LangSmith?
3. How could you tie token usage to budget enforcement for cost control?
""")

# --- LangSmith Tracing Example ---
init_langsmith()
response = run_agent_with_trace(agent, "Calculate 12 * 15 using the calculator tool")
print("Agent result:", response)
