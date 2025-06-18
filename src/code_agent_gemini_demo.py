#!/usr/bin/env python3

from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import OpenAIServerModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]
additional_authorized_imports = []

import dotenv
import os
dotenv.load_dotenv()

model_id="gemini-1.5-flash"
model_id="gemini-2.5-flash"
model = OpenAIServerModel(model_id=model_id,
                          api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
                          api_key=os.getenv("GEMINI_API_KEY"),
                          )
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=additional_authorized_imports,
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
