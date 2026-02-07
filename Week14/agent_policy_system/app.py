import os
from dotenv import load_dotenv
from core.agent import Agent
from core.policy_engine import PolicyEngine, ResponsePolicy
from core.evaluator import Evaluator
from core.memory import PolicyMemory
from observability.langsmith import validate_tracing_config, get_trace_context

# Load environment variables
load_dotenv()

# import os
# os.environ["LANGCHAIN_TRACING_V2"] = "false"

def main():
    print("=== Agentic AI Policy Adaptation System ===")
    
    # 1. Setup
    validate_tracing_config()
    
    memory = PolicyMemory("data/policy_history.json")
    agent = Agent()
    evaluator = Evaluator()
    
    # 2. Load current policy
    policy = memory.load_latest_policy()
    print(f"\n[Current Policy]: {policy.to_dict()}")
    
    # 3. Task Input
    user_task = input("\nEnter a task for the agent (e.g., 'Explain quantum computing'): ")
    if not user_task: user_task = "Explain quantum computing components"
    
    # 4. Initial Run
    print("\n--- Generating Initial Response ---")
    with get_trace_context(run_name="Initial Agent Run", tags=["policy_v1"], metadata={"policy": policy.to_dict()}):
        response_1 = agent.generate_response(user_task, policy)
    
    print(f"\n[Agent]: {response_1}")
    
    # 5. Feedback Collection
    feedback = input("\n[Feedback] How should the agent improve? (e.g., 'Too detailed, make it shorter'): ")
    if not feedback: 
        print("No feedback provided. Exiting.")
        return

    # 6. Evaluation & Policy Update
    print("\n--- Evaluating Feedback ---")
    with get_trace_context(run_name="Feedback Evaluation", tags=["evaluator"], metadata={"feedback": feedback}):
        delta = evaluator.evaluate_feedback(feedback, policy)
    
    if not delta:
        print("No policy change required based on feedback.")
        return
        
    print(f"[Policy Delta]: {delta}")
    
    new_policy = PolicyEngine.apply_delta(policy, delta)
    
    # Validate new policy (optional, but good practice)
    if not PolicyEngine.validate_policy(new_policy):
        print("Error: Proposed policy is invalid. Aborting update.")
        return

    print(f"[New Policy]: {new_policy.to_dict()}")
    
    # 7. Persist Change
    memory.save_entry(feedback, policy, new_policy, delta)
    print("Policy updated and saved.")
    
    # 8. Adapted Run
    print("\n--- Generating Adapted Response ---")
    with get_trace_context(run_name="Adapted Agent Run", tags=["policy_v2", "adapted"], metadata={"policy": new_policy.to_dict(), "feedback": feedback}):
        response_2 = agent.generate_response(user_task, new_policy)
        
    print(f"\n[Adapted Agent]: {response_2}")
    print("\nCheck LangSmith for traces of this interaction.")

if __name__ == "__main__":
    main()
