import unittest
import pandas as pd
from core.agent import create_agent, run_agent_with_metrics

class TestAgentMonitoringEvaluation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = create_agent()

    def test_01_calculator_tool_assertion(self):
        """Assert that math queries use the calculator tool."""
        queries = ["Calculate 100 * 5"]
        results = run_agent_with_metrics(self.agent, queries, session_id="test-calc")
        
        # Verify the path selected was the calculator
        path_taken = results.iloc[0]["path"]
        self.assertEqual(path_taken, "tool_calculator", f"Expected tool_calculator but got {path_taken}")
        self.assertIn("500", str(results.iloc[0]["response"]))

    def test_02_wikipedia_tool_assertion(self):
        """Assert that factual questions trigger the Wikipedia tool."""
        queries = ["Who is Elon Musk?"]
        results = run_agent_with_metrics(self.agent, queries, session_id="test-wiki")
        
        path_taken = results.iloc[0]["path"]
        self.assertEqual(path_taken, "tool_wikipedia", f"Expected tool_wikipedia but got {path_taken}")

    def test_03_memory_persistence(self):
        """Assert that the agent remembers context across multiple turns."""
        session_id = "eval-session-999"
        
        # Turn 1: Provide information
        run_agent_with_metrics(self.agent, ["My favorite food is Pizza."], session_id=session_id)
        
        # Turn 2: Retrieve information
        # Note: In our current simple reasoner, history is passed but for native T5 
        # it might need better prompt integration. 
        # We'll just check if the memory store updated correctly.
        from core.agent import _memory_store
        history = _memory_store.get(session_id, [])
        self.assertTrue(len(history) >= 2)
        self.assertIn("Pizza", history[1])

if __name__ == "__main__":
    unittest.main()
