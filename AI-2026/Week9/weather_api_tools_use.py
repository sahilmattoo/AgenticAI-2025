#This file contains code snippets for creating and using a weather tool with an agent in LangChain

# To do: create api key and keep in env file as WEATHER_API_KEY from this url: https://www.weatherapi.com/

# do the changes as per langchain 0.3.x version
import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Load environment variables first
load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")  # Check exact name

print("DEBUG: API Key Loaded:", bool(API_KEY))  # Optional test

@tool
def get_weather(city: str) -> str:
    """Fetch current weather using WeatherAPI."""
    if not API_KEY:
        return "Error: API key missing. Check your .env file."

    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)

    if response.status_code != 200:
        return f"API error: {response.text}"

    data = response.json()
    temp = data["current"]["temp_c"]
    cond = data["current"]["condition"]["text"]
    return f"Weather in {city}: {temp}°C, {cond}."


# LLM + agent
model = ChatOpenAI(model="gpt-4o-mini")
from langchain_core.prompts import ChatPromptTemplate

prompt_template =ChatPromptTemplate.from_template("""
You are an expert weather assistant. Use the tools provided to answer weather-related queries accurately.
User Request: {input},
("{agent_scratchpad}"
"""
)

tools = [get_weather]
agent = create_tool_calling_agent(llm=model, tools=tools, prompt=prompt_template)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=1)
# Test the agent with a sample query

query = "What's the weather in London right now?"
result = executor.invoke({"input": query})
print("Agent Output:", result)
  