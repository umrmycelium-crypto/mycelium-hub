"""
Secure Configuration Management for Mycelium OS
Loads sensitive configuration from environment variables.
"""

import os
from typing import Optional


def get_mistral_api_key() -> Optional[str]:
    """
    Safely retrieve Mistral API key from environment variables.
    
    Priority order:
    1. MISTRAL_API_KEY environment variable
    2. Returns None if not set
    
    Returns:
        The API key string, or None if not configured
    """
    return os.environ.get("MISTRAL_API_KEY")


def get_ollama_url() -> str:
    """
    Get Ollama service URL from environment or use default.
    """
    return os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")


def get_llamacpp_url() -> str:
    """
    Get Llamacpp service URL from environment or use default.
    """
    return os.environ.get("LLAMACPP_URL", "http://127.0.0.1:8080/v1/chat/completions")


def get_mistral_api_url() -> str:
    """
    Get Mistral API URL from environment or use default.
    """
    return os.environ.get("MISTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")


def is_mistral_configured() -> bool:
    """
    Check if Mistral API is configured with a key.
    """
    return get_mistral_api_key() is not None


def require_mistral_key() -> str:
    """
    Get Mistral API key, raising an error if not configured.
    
    Returns:
        The API key string
        
    Raises:
        RuntimeError: If MISTRAL_API_KEY is not set
    """
    key = get_mistral_api_key()
    if key is None:
        raise RuntimeError(
            "Mistral API key not configured. "
            "Please set the MISTRAL_API_KEY environment variable.\n"
            "Example: export MISTRAL_API_KEY='your-key-here'"
        )
    return key
