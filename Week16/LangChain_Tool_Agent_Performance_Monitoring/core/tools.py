"""
Module: Tools
Defines the agent tools — Wikipedia search and Python calculator.
"""

from langchain.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool

wiki = WikipediaAPIWrapper()
calc_tool = PythonREPLTool()

@tool
def wikipedia_search(query: str) -> str:
    """Search and summarize information from Wikipedia."""
    return wiki.run(query)

@tool
def calculator(expression: str) -> str:
    """Perform arithmetic or mathematical calculations."""
    return calc_tool.run(expression)

tools = [wikipedia_search, calculator]
