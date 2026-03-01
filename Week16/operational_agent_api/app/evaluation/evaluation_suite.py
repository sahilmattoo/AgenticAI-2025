"""
Evaluation Suite.
Defines the logic for evaluating agent performance and behavior boundaries.
Independent of the API deployment.
"""
from typing import Dict, List, Tuple

# Mock data for evaluation
EVAL_CASES = [
    {
        "input": "What is the system status?",
        "expected_route": "rule",
        "description": "Operational Status Query"
    },
    {
        "input": "How do I reset my password?",
        "expected_route": "agent",
        "description": "How-to Question"
    },
    {
        "input": "Show me the version",
        "expected_route": "rule",
        "description": "Version Query"
    },
    {
        "input": "Write a poem about scaling",
        "expected_route": "agent",
        "description": "Creative/Complex Task"
    }
]

def evaluate_routing_logic(router_func) -> List[Dict]:
    """
    Tests the router against a defined set of cases.
    """
    results = []
    for case in EVAL_CASES:
        predicted = router_func(case["input"])
        passed = predicted == case["expected_route"]
        results.append({
            "case": case["description"],
            "input": case["input"],
            "expected": case["expected_route"],
            "actual": predicted,
            "passed": passed
        })
    return results

def evaluate_memory_persistence(memory_store_instance, session_id: str) -> bool:
    """
    Verifies that memory persists interactions.
    """
    # 1. Add interaction
    memory_store_instance.add_message(session_id, "user", "test_interaction")
    
    # 2. Retrieve
    history = memory_store_instance.get_history(session_id)
    
    # 3. Verify
    has_message = any(msg["content"] == "test_interaction" for msg in history)
    return has_message
