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
def getenv(variable):
    global g_dotenv_loaded
    if not g_dotenv_loaded:
        g_dotenv_loaded = True
        dotenv.load_dotenv()
    value = os.getenv(variable)
    return value

def main():
    best_device = get_best_device()
    print(f"The best device is {best_device}.")
    
    key_value = getenv("GEMINI_API_KEY")
    if key_value:
        print("Have value for GEMINI_API_KEY.")
    else:
        print("Do not have value for GEMINI_API_KEY.")

    return

if __name__ == "__main__":
    main()

