import os
import time
from dotenv import load_dotenv
from core.agent import Agent
from core.policy_engine import PolicyEngine
from core.evaluator import Evaluator
from core.memory import PolicyMemory
from observability.langsmith import validate_tracing_config, get_trace_context

# Load environment variables from .env explicitly
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
loaded = load_dotenv(env_path, override=True)
print(f"Loading .env from: {env_path} | Success: {loaded}")
print(f"DEBUG: LANGCHAIN_API_KEY set? {'Yes' if os.getenv('LANGCHAIN_API_KEY') else 'No'}")
print(f"DEBUG: LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")

def run_automated_demo():
    print("=== Starting Automated Agent Policy Demo ===")
    
    # 1. Setup
    validate_tracing_config()
    
    # Initialize components with absolute paths
    data_path = os.path.join(script_dir, "data", "policy_history.json")
    memory = PolicyMemory(data_path)
    agent = Agent()
    evaluator = Evaluator()
    
    # 2. Define Scenario
    user_task = "Explain how a bicycle works."
    simulated_feedback = "Too long and complicated. Explain it simply in bullet points."
    
    print(f"\n[Scenario Task]: {user_task}")
    print(f"[Scenario Feedback]: {simulated_feedback}")
    
    # 3. Load Policy (or default)
    # For this test, let's force a default policy to ensure clean state
    from core.policy_engine import ResponsePolicy
    policy = ResponsePolicy.default() 
    print(f"\n[Initial Policy]: {policy.to_dict()}")
    
    # 4. Run 1: Default Policy
    print("\n--- 1. Generating Initial Response... ---")
    start_time = time.time()
    with get_trace_context(run_name="Auto-Demo: Initial Run", tags=["auto-test", "policy_v1"], metadata={"policy": policy.to_dict()}):
        response_1 = agent.generate_response(user_task, policy)
    print(f"Response generated in {time.time() - start_time:.2f}s")
    print(f"[Agent Response 1]: {response_1[:100]}... (truncated)")

    # 5. Evaluate Feedback
    print("\n--- 2. Evaluating Feedback... ---")
    with get_trace_context(run_name="Auto-Demo: Feedback Eval", tags=["auto-test", "evaluator"], metadata={"feedback": simulated_feedback}):
        delta = evaluator.evaluate_feedback(simulated_feedback, policy)
        
    print(f"[Evaluated Delta]: {delta}")
    
    if not delta:
        print("ERROR: Evaluator failed to produce a delta from clear feedback.")
        return

    # 6. Update Policy
    new_policy = PolicyEngine.apply_delta(policy, delta)
    print(f"[New Policy]: {new_policy.to_dict()}")
    
    # 7. Run 2: Adapted Policy
    print("\n--- 3. Generating Adapted Response... ---")
    with get_trace_context(run_name="Auto-Demo: Adapted Run", tags=["auto-test", "policy_v2", "adapted"], metadata={"policy": new_policy.to_dict()}):
        response_2 = agent.generate_response(user_task, new_policy)
        
    print(f"[Agent Response 2]: {response_2[:100]}... (truncated)")
    
    print("\n=== Demo Complete ===")
    print("Please check LangSmith for a trace named 'Auto-Demo: ...'")

if __name__ == "__main__":
    try:
        run_automated_demo()
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
