#!/usr/bin/env python3

###
# Device selection
###
import torch
def get_best_device():
    """Chooses the best device available.
    CUDA
    MPS
    CPU
    """
    if torch.cuda.is_available():
        # For NVIDIA GPUs
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        # For Apple Silicon (M1/M2/M3)
        return torch.device("mps")
    else:
        # Fallback to CPU
        return torch.device("cpu")

###
# Environment loading
###
import dotenv
import os
g_dotenv_loaded = False
def getenv(variable: str) -> str:
    global g_dotenv_loaded
    if not g_dotenv_loaded:
        g_dotenv_loaded = True
        dotenv.load_dotenv()
    value = os.getenv(variable)
    return value


###
# Ollama model checking
###
import requests
OLLAMA_BASE_URL = "http://localhost:11434"
def is_ollama_model_installed(model_id: str, base_url: str = OLLAMA_BASE_URL) -> bool:
    """Checks if a specific model tag exists on the Ollama server."""
    try:
        # Ollama's /api/tags endpoint lists all locally available models
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        
        # Check if the model tag is in the list of 'models'
        for model in data.get("models", []):
            if model.get("name") == model_id:
                return True
        
        return False

    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Ollama server at {base_url}. Is Ollama running?")
        return False
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred while querying Ollama: {e}")
        return False

def main():
    best_device = get_best_device()
    print(f"The best device is {best_device}.")
    
    key_value = getenv("GEMINI_API_KEY")
    if key_value:
        print("Have value for GEMINI_API_KEY.")
    else:
        print("Do not have value for GEMINI_API_KEY.")

    model_id = "llama3.1:405b"
    if is_ollama_model_installed(model_id):
        print(f"{model_id} is installed")
    else:
        print(f"{model_id} is not installed")

    return

if __name__ == "__main__":
    main()

