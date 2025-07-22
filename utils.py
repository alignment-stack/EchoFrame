"""
EchoFrame Utility Functions
Author: Alignment Stack
Version: 0.1
"""
import os
import psutil
from llama_cpp import Llama

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')

def scan_models_folder(models_path: str) -> list:
    """Scan the /models folder for .gguf files (compatible with UI)."""
    return [f for f in os.listdir(models_path) if f.endswith('.gguf')]

def load_model(model_path):
    """Load a .gguf model using llama-cpp-python."""
    return Llama(model_path=model_path)

def get_model_metadata(model_path):
    """Return basic metadata for a .gguf model."""
    model = Llama(model_path=model_path)
    return {
        'context_window': getattr(model, 'n_ctx', None),
        'params': getattr(model, 'params', None),
        'size_mb': os.path.getsize(model_path) // (1024 * 1024),
        'estimated_ram': psutil.virtual_memory().total // (1024 * 1024)
    }

def estimate_tokens(text):
    """Estimate token count (simple whitespace split)."""
    return len(text.split())
