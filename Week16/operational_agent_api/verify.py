import sys
import os

# Add app to path
sys.path.append(os.getcwd())

from app.evaluation.evaluation_suite import evaluate_routing_logic, evaluate_memory_persistence
from app.core.router import route_request
from app.core.memory import SessionMemory
import uuid

def run_checks():
    print("Running Verification Checks...")
    
    # Check 1: Routing
    print("\n1. Testing Routing Logic...")
    results = evaluate_routing_logic(route_request)
    failures = [r for r in results if not r["passed"]]
    if failures:
        print(f"FAILED: {failures}")
    else:
        print("PASSED: all routing cases confirmed.")

    # Check 2: Memory
    print("\n2. Testing Memory Persistence...")
    mem = SessionMemory()
    sid = str(uuid.uuid4())
    success = evaluate_memory_persistence(mem, sid)
    if success:
        print("PASSED: Memory persistence confirmed.")
    else:
        print("FAILED: Memory did not persist.")

    print("\nVerification Complete.")

if __name__ == "__main__":
    run_checks()
