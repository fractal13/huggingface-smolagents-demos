#!/usr/bin/env python3
from demo_utils import get_best_device
device = get_best_device()

from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import TransformersModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]
additional_authorized_imports = []

# Must be image-text-to-text
model_id = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"
model_id = "HuggingFaceTB/SmolVLM-500M-Instruct"

import torch
torch.cuda.empty_cache()

model = TransformersModel(model_id=model_id, device_map=device)

from smolagents import LogLevel
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=additional_authorized_imports,
    max_steps=5,
    verbosity_level = LogLevel.DEBUG
)

answer = agent.run("What events are happening in Pokemon GO today?")
print(f"Agent returned answer: {answer}")
