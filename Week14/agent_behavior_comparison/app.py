import os
import time
from dotenv import load_dotenv
from core.static_router import StaticRouter
from core.routing_agent import RoutingAgent
from core.policy_engine import PolicyEngine, RoutingPolicy
from core.evaluator import Evaluator
from core.memory import PolicyMemory
from observability.langsmith import validate_tracing, get_trace_context

# Load environment variables
load_dotenv(override=True)

def run_static_mode():
    print("\n[MODE] STATIC DETECTED (Week 9)")
    print("Logic: Keyword Matching | State: None | Feedback: Ignored")
    
    while True:
        query = input("\n[Static] Enter Query (or 'exit'): ")
        if query.lower() in ["exit", "quit"]: break
        
        start = time.time()
        result = StaticRouter.route_query(query)
        duration = time.time() - start
        
        print(f" -> Routing Decision: {result} ({duration:.4f}s)")
        print(" -> [Log] No Trace sent to LangSmith.")

def run_adaptive_mode():
    print("\n[MODE] ADAPTIVE DETECTED (Week 14)")
    print("Logic: LLM + Policy | State: Persistent | Feedback: Active")
    
    if validate_tracing():
        print(" -> LangSmith Tracing: ENABLED ✅")
    else:
        print(" -> LangSmith Tracing: DISABLED ⚠️ (Check .env)")

    # Init Components
    memory_path = os.path.join(os.getcwd(), 'agent_behavior_comparison', 'data', 'policy_history.json')
    # If running from inner folder, adjust path logic or rely on CWD.
    if not os.path.exists(os.path.dirname(memory_path)):
        # Fallback for different CWDs
        memory_path = "data/policy_history.json"
        
    memory = PolicyMemory(memory_path)
    agent = RoutingAgent()
    evaluator = Evaluator()
    
    while True:
        # Load latest policy
        current_policy = memory.load_latest_policy()
        print(f"\n[Active Policy]: Priority={current_policy.routing_priority}")
        
        query = input("\n[Adaptive] Enter Query (or 'exit'): ")
        if query.lower() in ["exit", "quit"]: break
        
        # Run Agent
        with get_trace_context(run_name="Adaptive Routing", tags=["adaptive", "v2"]):
            result = agent.run(query, current_policy)
        
        print(f" -> Decision: {result.get('department')} (Conf: {result.get('confidence')})")
        print(f" -> Reasoning: {result.get('reasoning')}")
        
        # Feedback Loop
        feedback = input("[Feedback] Correct? (Enter to skip, or type feedback): ")
        if feedback:
            print(" -> Evaluating feedback...")
            with get_trace_context(run_name="Feedback Evaluation", tags=["evaluator"]):
                delta = evaluator.evaluate_feedback(feedback, current_policy)
            
            if delta:
                print(f" -> Policy Delta Identified: {delta}")
                new_policy = PolicyEngine.apply_delta(current_policy, delta)
                memory.save_entry(feedback, current_policy, new_policy, delta)
                print(" -> Policy Updated! 🔄")
            else:
                print(" -> No policy change needed.")

def main():
    print("=== Agent Behavior Comparison System ===")
    print("1. Static Mode (Legacy Rule-Based)")
    print("2. Adaptive Mode (Policy-Driven)")
    
    choice = input("Select Mode (1/2): ")
    
    if choice == "1":
        run_static_mode()
    elif choice == "2":
        run_adaptive_mode()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
