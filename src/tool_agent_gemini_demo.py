#!/usr/bin/env python3

from demo_utils import getenv
api_key = getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY needs to be set in .env.")

from smolagents import ToolCallingAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import OpenAIServerModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]

model_id="gemini-1.5-flash"
model_id="gemini-2.5-flash"
model = OpenAIServerModel(model_id=model_id,
                          api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
                          api_key=api_key,
                          )
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    max_steps=5
)

answer = agent.run("What events are happening in Pokemon GO today?")
print(f"Agent returned answer: {answer}")


"""
https://aistudio.google.com/ "Get API key"
https://aistudio.google.com/apikey
Use OpenAIServerModel due to API compatibility
[Select model](https://ai.google.dev/gemini-api/docs/models)

"""
