# ===== MCP SERVER (Simulated) =====

def fetch_portfolio(user_id):
    # Simulated enterprise data (DB / API / ERP)
    return {
        "user_id": user_id,
        "holdings": [
            {"symbol": "INFY", "value": 120000},
            {"symbol": "TCS", "value": 90000},
            {"symbol": "HDFC", "value": 140000}
        ],
        "total_value": 350000
    }

# MCP tool registry
MCP_TOOLS = {
    "fetch_portfolio": fetch_portfolio
}

def mcp_call(tool_name, arguments):
    if tool_name not in MCP_TOOLS:
        return {"error": "Tool not allowed"}
    return MCP_TOOLS[tool_name](**arguments)


# ===== CREWAI TOOL (Wrapper over MCP) =====

from crewai import tool, Agent, Task, Crew

@tool
def get_user_portfolio(user_id: str):
    """Fetch user's portfolio using MCP"""
    return mcp_call(
        tool_name="fetch_portfolio",
        arguments={"user_id": user_id}
    )


# ===== CREWAI AGENT =====

portfolio_agent = Agent(
    role="Portfolio Analyst",
    goal="Analyse user's investment portfolio",
    backstory="Expert financial analyst who explains insights clearly",
    tools=[get_user_portfolio]
)


# ===== CREWAI TASK =====

task = Task(
    description="Analyse portfolio of user U123 and summarize investment exposure",
    agent=portfolio_agent
)


# ===== CREW EXECUTION =====

crew = Crew(
    agents=[portfolio_agent],
    tasks=[task]
)

result = crew.kickoff()
print(result)


"""
Agent does NOT call business logic directly

CrewAI agent → MCP tool → enterprise capability

MCP controls:

    What tools exist

    What data is returned

CrewAI controls:

    easoning

    Planning

    Language output 


"""