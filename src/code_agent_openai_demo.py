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

model = OpenAIServerModel(model_id="gpt-4o",
                          api_base="https://api.openai.com/v1",
                          api_key=os.getenv("OPENAI_API_KEY"),
                          )
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=additional_authorized_imports,
    max_steps=5
)

answer = agent.run("What events are happening in Pokemon GO today?")
print(f"Agent returned answer: {answer}")
