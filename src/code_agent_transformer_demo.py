#!/usr/bin/env python3

from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import TransformersModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]
additional_authorized_imports = []

# Must be image-text-to-text
# These two don't give good results
# HuggingFaceTB/SmolVLM-256M-Instruct
# HuggingFaceTB/SmolVLM-500M-Instruct
# This one won't load in the GPU
# HuggingFaceTB/SmolVLM2-2.2B-Instruct
# model = TransformersModel(model_id="HuggingFaceTB/SmolVLM2-2.2B-Instruct", max_new_tokens=16384)

import torch
torch.cuda.empty_cache()

model = TransformersModel(model_id="HuggingFaceTB/SmolVLM2-2.2B-Instruct", 
                          torch_dtype=torch.float16,
                          max_new_tokens=16384)

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
