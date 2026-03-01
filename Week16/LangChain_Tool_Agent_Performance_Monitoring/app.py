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
try:
    report = generate_drift_report(ref_metrics, cur_metrics)
except Exception as e:
    print(f"[WARNING] Drift report generation failed: {e}")
    print("This is likely due to Pydantic v1 compatibility issues on Python 3.14.")

# --- Show Reflection ---
# --- Summary Output ---
print("\n[INFO] Monitoring Pipeline Complete.")
print(f"- Drift Report: reports/drift_report.html")
print(f"- Trace Destination: LangSmith Project 'Agent_Performance_Monitoring'")

# --- Single Diagnostic Trace ---
print("\n[INFO] Executing Diagnostic Trace...")
init_langsmith()
response = run_agent_with_trace(agent, "Calculate 12 * 15")
print(f"Diagnostic Result: {response}")
