# huggingface-smolagents-demos
Simple demos of syntax for using smolagents from Hugging Face.


## TransformersModel

Unable to get this to fit in the GPU memory at this time.

One of the issues is the requirement that the mode is image-text-to-text, instead
of allowing text-to-text models. The image-text-to-text have larger footprint.

There is a quick and dirty hack to make a smaller model with quantized weights,
but it still does not fit in the GPU memory. This was based on a pull request to 
the smolagents repo, that has not be merged. Since that is two months old, I'm 
going to assume it won't be merged. 
[Pull Request](https://github.com/huggingface/smolagents/pull/1174)

I'll put this example on hold for now. Possible solutions:

1- bigger GPU memory
2- make a TransformersModel subclass that works with text-to-text models.

## LiteLLMModel (ollama)

Access model in ollama via the LiteLLMModel class. This demo offloads the
model loading to ollama.

## Network API Models

### OpenAIServerModel

- Need api key. Store in `.env/OPENAI_API_KEY`. Use dotenv to load it.
- [smolagents.OpneAIServerModel](https://huggingface.co/docs/smolagents/en/reference/models#smolagents.OpenAIServerModel)
- [OpenAI API](https://openai.com/api/)

### Something for Gemini

- Need API key. Store in `.env/OPENAI_API_KEY`. Use dotenv to load it.
- [Create API Key](https://aistudio.google.com/) "Get API key"
- Not sure on billing yet.
- Use `OpenAIServerModel` due to API compatibility
- [Select model](https://ai.google.dev/gemini-api/docs/models)
- `api_base="https://generativelanguage.googleapis.com/v1beta/openai/"`

### Something for hugging face?

- TODO

### Other Services?


