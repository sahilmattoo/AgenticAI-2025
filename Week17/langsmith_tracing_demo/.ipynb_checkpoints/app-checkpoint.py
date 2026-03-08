"""
Main entry point — runs the demo queries using the traceable agent.
"""

from core.traceable_chain import ask_agent

def main():
    queries = [
        "Who discovered penicillin?",
        "Explain the difference between AI and machine learning.",
        "What is the square root of 256?"
    ]

    for q in queries:
        print(f"Query: {q}")
        print("Answer:", ask_agent(q))
        print("-" * 80)

if __name__ == "__main__":
    main()
