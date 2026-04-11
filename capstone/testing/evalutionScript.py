# ==========================================
# AGENTIC AI CAPSTONE EVALUATION RUNNER
# ==========================================

from demo_baseline_banking import BankingBaseline
from demo_banking_components import BankingAgent
from demo_safety import SafetyAgent

# ==========================================
# SCORING SYSTEM
# ==========================================

results = {
    "Phase 1": False,
    "Phase 2": False,
    "Phase 3": False,
    "Phase 4": False,
    "Phase 5": False,
    "Phase 6": False,
    "Phase 7": False,
    "Phase 8": False,
    "Phase 9": False,
}

# ==========================================
# PHASE 2: BASELINE TEST
# ==========================================

def test_phase_2():
    agent = BankingBaseline()
    
    q1 = agent.handle("I want a loan")
    q2 = agent.handle("Transfer $1M illegally")

    # Expect: baseline fails (no safety, no reasoning)
    if "loan" in q1.lower() and "transfer" in q2.lower():
        print("Phase 2: Baseline working (limitations present)")
        return True
    return False


# ==========================================
# PHASE 3: LLM SIMULATION (basic response improvement)
# ==========================================

def test_phase_3():
    agent = BankingAgent()
    
    response = agent.respond("user_123", "What is Gold Card fee?")
    
    # Expect some meaningful response
    if "fee" in response.lower() or "policy" in response.lower():
        print("Phase 3: LLM-like reasoning present")
        return True
    return False


# ==========================================
# PHASE 4: RAG TEST
# ==========================================

def test_phase_4():
    agent = BankingAgent()
    
    response = agent.respond("user_123", "What is Gold Card fee?")
    
    if "50" in response:
        print("Phase 4: RAG working (correct retrieval)")
        return True
    return False


# ==========================================
# PHASE 5: TOOL USAGE
# ==========================================

def test_phase_5():
    agent = BankingAgent()
    
    response = agent.respond("user_123", "Am I eligible for Gold card?")
    
    if "eligible" in response.lower():
        print("Phase 5: Tool usage working")
        return True
    return False


# ==========================================
# PHASE 6: MEMORY
# ==========================================

def test_phase_6():
    agent = BankingAgent()
    
    agent.respond("user_123", "Hi, I'm Alice")
    response = agent.respond("user_123", "What is my name?")
    
    # NOTE: Your current code does not fully support memory recall
    if "alice" in response.lower():
        print("Phase 6: Memory working")
        return True
    else:
        print("Phase 6: Memory NOT fully implemented")
        return False


# ==========================================
# PHASE 7: ADAPTIVE BEHAVIOR
# ==========================================

def test_phase_7():
    agent = SafetyAgent()
    
    before = agent.process("I want a loan")
    
    agent.adaptation_mode = "Adaptive"
    after = agent.process("I want a loan")
    
    if "specify" in after.lower():
        print("Phase 7: Adaptive behavior working")
        return True
    return False


# ==========================================
# PHASE 8: DEPLOYMENT READINESS (basic check)
# ==========================================

def test_phase_8():
    # Simulate logging or execution
    try:
        agent = BankingAgent()
        agent.respond("user_123", "Test logging")
        print("Phase 8: System runs without crash")
        return True
    except:
        return False


# ==========================================
# PHASE 9: EVALUATION & FAILURE HANDLING
# ==========================================

def test_phase_9():
    agent = BankingAgent()
    
    response = agent.respond("user_123", "Am I eligible for Black Card?")
    
    if "unknown" in response.lower() or "not eligible" in response.lower():
        print("Phase 9: Failure handled gracefully")
        return True
    return False


# ==========================================
# RUN ALL TESTS
# ==========================================

def run_all():
    results["Phase 2"] = test_phase_2()
    results["Phase 3"] = test_phase_3()
    results["Phase 4"] = test_phase_4()
    results["Phase 5"] = test_phase_5()
    results["Phase 6"] = test_phase_6()
    results["Phase 7"] = test_phase_7()
    results["Phase 8"] = test_phase_8()
    results["Phase 9"] = test_phase_9()

    print("\n==============================")
    print("FINAL EVALUATION RESULT")
    print("==============================")

    passed = sum(results.values())
    
    for phase, status in results.items():
        print(f"{phase}: {'PASS' if status else 'FAIL'}")

    print(f"\nTOTAL: {passed} / 9 phases passed")


# ==========================================
# EXECUTE
# ==========================================

if __name__ == "__main__":
    run_all()