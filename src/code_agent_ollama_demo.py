#!/usr/bin/env python3

from demo_utils import is_ollama_model_installed
model_id_list = ["llama3.1:405b", "qwen3:8b"]
model_id = None
for tmp_model_id in model_id_list:
    if is_ollama_model_installed(tmp_model_id):
        model_id = tmp_model_id
        break
if not model_id:
    raise Exception(f"None of {model_id_list} are installed in ollama.")

from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import LiteLLMModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]
additional_authorized_imports = []

model = LiteLLMModel(model_id=f"ollama_chat/{model_id}", api_base="http://127.0.0.1:11434")
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=additional_authorized_imports,
    max_steps=5
)

answer = agent.run("What events are happening in Pokemon GO today?")
print(f"Agent returned answer: {answer}")
