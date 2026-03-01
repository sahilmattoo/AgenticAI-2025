"""
Evaluation Tests.
Runs the evaluation suite logic against the codebase.
"""
import pytest
import uuid
from app.core.router import route_request
from app.core.memory import SessionMemory
from app.evaluation.evaluation_suite import evaluate_routing_logic, evaluate_memory_persistence

def test_routing_evaluation():
    """
    Runs the deterministic routing evaluation suite.
    """
    results = evaluate_routing_logic(route_request)
    
    failures = [r for r in results if not r["passed"]]
    
    assert len(failures) == 0, f"Routing evaluation failed for cases: {failures}"

def test_memory_persistence_logic():
    """
    Validates independent memory persistence logic.
    """
    mem = SessionMemory()
    session_id = str(uuid.uuid4())
    
    success = evaluate_memory_persistence(mem, session_id)
    assert success, "Memory failed to persist interaction"
    
    # Check persistence across multiple adds
    mem.add_message(session_id, "assistant", "response")
    history = mem.get_history(session_id)
    assert len(history) == 2, "Memory should have 2 messages"

def test_memory_session_isolation():
    """
    Ensures data does not leak between sessions.
    """
    mem = SessionMemory()
    s1 = "session_1"
    s2 = "session_2"
    
    mem.add_message(s1, "user", "secret_1")
    mem.add_message(s2, "user", "secret_2")
    
    hist1 = mem.get_history(s1)
    hist2 = mem.get_history(s2)
    
    assert len(hist1) == 1
    assert hist1[0]["content"] == "secret_1"
    assert len(hist2) == 1
    assert hist2[0]["content"] == "secret_2"
