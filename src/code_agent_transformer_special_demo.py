#!/usr/bin/env python3

from smolagents import CodeAgent
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool
from smolagents import TransformersModel

search_tool = DuckDuckGoSearchTool()
visit_webpage_tool = VisitWebpageTool()
tools = [ search_tool, visit_webpage_tool ]
additional_authorized_imports = []

class SpecialTransformersModel(TransformersModel):
    """Attempt to allow using preloaded models, so we can do smaller footprint.

    Failed.
    """

    def __init__(
        self,
        model = None,
        model_id: str | None = None,
        device_map: str | None = None,
        torch_dtype: str | None = None,
        trust_remote_code: bool = False,
        **kwargs,
    ):
        try:
            import torch
            from transformers import (
                AutoModelForCausalLM,
                AutoModelForImageTextToText,
                AutoProcessor,
                AutoTokenizer,
                TextIteratorStreamer,
            )
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install 'transformers' extra to use 'TransformersModel': `pip install 'smolagents[transformers]'`"
            )

        if not model_id:
            warnings.warn(
                "The 'model_id' parameter will be required in version 2.0.0. "
                "Please update your code to pass this parameter to avoid future errors. "
                "For now, it defaults to 'HuggingFaceTB/SmolLM2-1.7B-Instruct'.",
                FutureWarning,
            )
            model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

        if model is None:
            default_max_tokens = 4096
            max_new_tokens = kwargs.get("max_new_tokens") or kwargs.get("max_tokens")
            if not max_new_tokens:
                kwargs["max_new_tokens"] = default_max_tokens
                logger.warning(
                    f"`max_new_tokens` not provided, using this default value for `max_new_tokens`: {default_max_tokens}"
                )

            if device_map is None:
                device_map = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device_map}")
            self._is_vlm = False
            try:
                self.model = AutoModelForImageTextToText.from_pretrained(
                    model_id,
                    device_map=device_map,
                    torch_dtype=torch_dtype,
                    trust_remote_code=trust_remote_code,
                )
                self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=trust_remote_code)
                self._is_vlm = True
                self.streamer = TextIteratorStreamer(self.processor.tokenizer, skip_prompt=True, skip_special_tokens=True)  # type: ignore

            except ValueError as e:
                if "Unrecognized configuration class" in str(e):
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_id,
                        device_map=device_map,
                        torch_dtype=torch_dtype,
                        trust_remote_code=trust_remote_code,
                    )
                    self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=trust_remote_code)
                    self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)  # type: ignore
                else:
                    raise e
            except Exception as e:
                raise ValueError(f"Failed to load tokenizer and model for {model_id=}: {e}") from e
        else:
            self.model = model

            self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=trust_remote_code)
            self._is_vlm = True
            self.streamer = TextIteratorStreamer(self.processor.tokenizer, skip_prompt=True, skip_special_tokens=True)  # type: ignore


        super().__init__(flatten_messages_as_text=not self._is_vlm, model_id=model_id, **kwargs)



from transformers import AutoModelForImageTextToText, QuantoConfig
model_id = "Qwen/Qwen2.5-VL-3B-Instruct"
quantization_config = QuantoConfig(weights="int8")
quantized_model = AutoModelForImageTextToText.from_pretrained(
    model_id, device_map="cuda", quantization_config=quantization_config
)

import torch
torch.cuda.empty_cache()

model = SpecialTransformersModel(model=quantized_model, model_id=model_id)

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
