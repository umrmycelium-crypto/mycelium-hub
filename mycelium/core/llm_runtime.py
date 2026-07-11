"""
Unified LLM Runtime for Mycelium OS
Supports multiple backends: Ollama, Llamacpp, and Mistral API
"""

import requests
import json
from typing import Optional, Dict, Any
from mycelium.core.models import (
    get_llm_model,
    OLLAMA_URL,
    LLAMACPP_URL,
    MISTRAL_API_URL,
    MISTRAL_API_KEY,
)


class LLMRuntime:
    """
    Unified runtime for calling LLM models across different backends.
    Automatically routes to the appropriate backend based on model name.
    """
    
    # Models served by llamacpp (local)
    LLAMACPP_MODELS = {"devstral"}
    
    # Models served by Mistral API (cloud)
    MISTRAL_MODELS = {"mistral-tiny", "mistral-small", "mistral-medium", "mistral-large"}
    
    @classmethod
    def call(cls, prompt: str, model: Optional[str] = None, 
             messages: Optional[list] = None, 
             temperature: float = 0.7,
             max_tokens: int = 2048) -> str:
        """
        Call an LLM model with the appropriate backend.
        
        Args:
            prompt: The text prompt (for Ollama)
            model: Model name to use (defaults to configured default)
            messages: Messages in chat format (for Mistral/OpenAI-compatible APIs)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            The model's text response
        """
        if model is None:
            model = get_llm_model()
        
        # Route to appropriate backend
        if model in cls.LLAMACPP_MODELS:
            return cls._call_llamacpp(prompt, model, temperature, max_tokens)
        elif model in cls.MISTRAL_MODELS or model.startswith("mistral-"):
            return cls._call_mistral(prompt, model, messages, temperature, max_tokens)
        else:
            # Default to Ollama
            return cls._call_ollama(prompt, model)
    
    @classmethod
    def _call_ollama(cls, prompt: str, model: str) -> str:
        """Call Ollama API"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        
        if response.status_code != 200:
            raise RuntimeError(f"Ollama error [{response.status_code}]: {response.text}")
        
        return response.json().get("response", "")
    
    @classmethod
    def _call_llamacpp(cls, prompt: str, model: str, 
                       temperature: float, max_tokens: int) -> str:
        """Call Llamacpp API (OpenAI-compatible endpoint)"""
        # Convert prompt to messages format
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                LLAMACPP_URL,
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code != 200:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get("error", {}).get("message", response.text)
                raise RuntimeError(
                    f"Llamacpp error [{response.status_code}]: {error_msg}"
                )
            
            # Handle response
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return str(result)
                
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"Cannot connect to llamacpp at {LLAMACPP_URL}. "
                "Is the server running?"
            )
    
    @classmethod
    def _call_mistral(cls, prompt: str, model: str, 
                      messages: Optional[list], 
                      temperature: float, max_tokens: int) -> str:
        """Call Mistral API"""
        if MISTRAL_API_KEY is None:
            raise RuntimeError(
                "Mistral API key not configured. "
                "Set MISTRAL_API_KEY in mycelium/core/models.py"
            )
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        
        # Build messages
        if messages is not None:
            msg_list = messages
        else:
            msg_list = [
                {"role": "user", "content": prompt}
            ]
        
        payload = {
            "model": model,
            "messages": msg_list,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(
                MISTRAL_API_URL,
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code != 200:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get("message", response.text)
                raise RuntimeError(
                    f"Mistral API error [{response.status_code}]: {error_msg}"
                )
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Mistral API request failed: {str(e)}")
    
    @classmethod
    def call_with_context(cls, system_prompt: str, user_prompt: str, 
                         model: Optional[str] = None,
                         temperature: float = 0.2, 
                         max_tokens: int = 2048) -> str:
        """
        Call an LLM with system and user prompts (for chat-style models).
        
        Args:
            system_prompt: System message
            user_prompt: User message
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            The model's response
        """
        if model is None:
            model = get_llm_model()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Route based on model type
        if model in cls.LLAMACPP_MODELS:
            # Llamacpp uses chat format
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(LLAMACPP_URL, json=payload, 
                                   headers=headers, timeout=120)
            
            if response.status_code != 200:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get("error", {}).get("message", response.text)
                raise RuntimeError(f"Llamacpp error: {error_msg}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        elif model in cls.MISTRAL_MODELS or model.startswith("mistral-"):
            # Mistral API
            return cls._call_mistral("", model, messages, temperature, max_tokens)
        else:
            # Ollama - combine into single prompt
            full_prompt = f"""<s>[INST] {system_prompt}

{user_prompt} [/INST]"""
            return cls._call_ollama(full_prompt, model)


def call_llm(prompt: str, model: Optional[str] = None) -> str:
    """
    Convenience function to call an LLM model.
    Backwards compatible with existing code.
    """
    return LLMRuntime.call(prompt, model)
