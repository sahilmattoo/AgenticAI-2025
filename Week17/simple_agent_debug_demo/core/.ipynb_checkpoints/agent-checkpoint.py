"""
Core logic for the simulated agent that occasionally fails.
"""

import random
import time
from core.logger import log_to_file

def simple_agent(query: str) -> str:
    """Simulated agent that occasionally breaks."""
    log_to_file(f"Received query: {query}")
    start = time.time()

    try:
        if "calc" in query.lower():
            # Randomly select a working or broken tool
            tool_name = "BrokenCalculator" if random.random() < 0.4 else "Calculator"
            log_to_file(f"Trying to use tool: {tool_name}")

            if tool_name == "Calculator":
                # Bug: naive parsing fails for inputs like "78*7"
                digits = [int(s) for s in query.replace("*", " ").split() if s.isdigit()]
                result = digits[0] * digits[1]
                log_to_file(f"Calculation successful: {result}")
                answer = f"The result is {result}"
            else:
                raise ValueError(f"Tool '{tool_name}' not found")
        else:
            answer = f"I don't know how to handle '{query}'"
            log_to_file("No valid tool found for this query")

    except Exception as e:
        log_to_file(f"Error occurred: {e}", error=True)
        answer = f"Agent failed due to: {e}"

    finally:
        elapsed = time.time() - start
        log_to_file(f"Query completed in {elapsed:.2f}s\n")

    return answer
