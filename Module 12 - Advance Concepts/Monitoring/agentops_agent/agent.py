from google.adk.agents.llm_agent import Agent


"""
agents.py
---------
Demo: Google ADK Agent + AgentOps Observability

This script shows how to integrate AgentOps with a Google ADK agent.
The agent can answer user questions about the time and weather in a city,
and every step (agent execution, tool calls, LLM calls) is captured in
the AgentOps dashboard for observability.

Steps:
1. Set AgentOps API key via environment variable.
2. Initialize AgentOps for telemetry.
3. Define a simple ADK Agent with two tools:
   - get_weather(city)
   - get_current_time(city)
4. Run the agent with sample queries.
"""

import os
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# Import Google ADK agent
from google.adk.agents import Agent

# Import AgentOps
import agentops


# ---------------------------
# 1. Load environment variables
# ---------------------------
load_dotenv()

# Directly set API key in env for demo (replace with your secure method in production)
os.environ["AGENTOPS_API_KEY"] = "f9bdfcdc-479c-429c-af90-59bf7a5027ea"


# ---------------------------
# 2. Initialize AgentOps
# ---------------------------
agentops.init(
    api_key=os.getenv("AGENTOPS_API_KEY"),
    trace_name="adk_weather_time_demo"
)


# ---------------------------
# 3. Define Tools
# ---------------------------
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city."""
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25°C (77°F)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}.",
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


# ---------------------------
# 4. Create ADK Agent
# ---------------------------
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about the time and weather in a city.",
    instruction="You are a helpful agent who can answer user questions about the time and weather in a city.",
    tools=[get_weather, get_current_time],
)
