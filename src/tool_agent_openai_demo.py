#!/usr/bin/env python3

from demo_utils import getenv
api_key = getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("OPENAI_API_KEY needs to be set in .env.")


from smolagents import ToolCallingAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import OpenAIServerModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]

model = OpenAIServerModel(model_id="gpt-4o",
                          api_base="https://api.openai.com/v1",
                          api_key=api_key,
                          )
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    max_steps=5
)

answer = agent.run("What events are happening in Pokemon GO today?")
print(f"Agent returned answer: {answer}")
