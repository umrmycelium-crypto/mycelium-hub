import json
import yaml
import requests
from pathlib import Path
from mycelium.core.intent_schema import validate_intent
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.models import get_llm_model, OLLAMA_URL
from mycelium.core.config import is_mistral_configured
from mycelium.core.llm_runtime import LLMRuntime

INTENTS_FILE = "mycelium/intents.yaml"

# Maximum context length to avoid hitting model limits
MAX_CONTEXT_LENGTH = 16000


def get_dynamic_system_prompt() -> str:
    """
    Generates a system prompt based on the semantic definitions in intents.yaml.
    """
    try:
        with open(INTENTS_FILE, 'r') as f:
            intents_data = yaml.safe_load(f) or {}
            
            intent_definitions = []
            for name, data in intents_data.items():
                desc = data.get('description', 'No description provided.')
                examples = ", ".join(data.get('examples', []))
                intent_definitions.append(f"- {name}: {desc} (Examples: {examples})")
            
            intent_list = "\n".join(intent_definitions)
    except Exception as e:
        print(f"Error loading intents: {e}")
        intent_list = "- system.status: Check system health"

    return f"""
You are the Local Brain for the Mycelium system. Your job is to parse natural language into a structured intent.

RULES:
- Output ONLY valid JSON.
- No explanations, no markdown, no extra text.
- Extract key entities (like movie titles, search queries, or filenames) into the 'payload' object.
- Use the provided 'Cognitive Context' to resolve references (like "it", "that one", "do it again").

Return format:
{{
  "intent": "...",
  "confidence": 0.0-1.0,
  "payload": {{
    "entity_name": "extracted_value"
  }},
  "requires_confirmation": false
}}

Semantic Intent Map:
{intent_list}

If uncertain:
- use confidence < 0.6
- set requires_confirmation = true
"""


def _truncate_context(prompt: str, max_length: int = MAX_CONTEXT_LENGTH) -> str:
    """Truncate prompt to fit within model context limits."""
    if len(prompt) <= max_length:
        return prompt
    
    # Try to truncate intelligently by removing older cognitive context
    # while preserving the system prompt and user input
    parts = prompt.split("\n\n")
    if len(parts) >= 3:
        # Structure: system_prompt + \n\n + Cognitive Context: + \n\n + User input:
        system_prompt = parts[0]
        cognitive_context = parts[1] if len(parts) > 1 else ""
        user_input = parts[-1] if len(parts) > 2 else ""
        
        # Truncate cognitive context
        context_header = "Cognitive Context:"
        if context_header in cognitive_context:
            context_content = cognitive_context.split(context_header)[-1]
            if len(system_prompt) + len(user_input) + len(context_header) + 100 < max_length:
                # Keep some context
                available_for_context = max_length - len(system_prompt) - len(user_input) - len(context_header) - 20
                truncated_context = context_content[-available_for_context:]
                return f"{system_prompt}\n\n{context_header}{truncated_context}\n\n{user_input}"
    
    # Fallback: simple truncation from the beginning
    return prompt[-max_length:]


def llm_to_intent(user_text: str, model: str = None) -> dict:
    """
    Converts natural language → validated Intent object using dynamic prompt and cognitive context.
    
    Args:
        user_text: The user input text
        model: Optional model override (defaults to configured default)
    """
    system_prompt = get_dynamic_system_prompt()
    cognitive_context = cognitive_state.get_snapshot()

    try:
        # We prime the LLM with the context before the user input
        full_prompt = f"{system_prompt}\n\nCognitive Context:\n{cognitive_context}\n\nUser input:\n{user_text}"
        
        # Truncate if too long
        full_prompt = _truncate_context(full_prompt)
        
        # Use the unified runtime
        raw_text = LLMRuntime.call(full_prompt, model=model)

        # Try parsing strict JSON
        data = json.loads(raw_text)

        # Validate through your existing system
        intent = validate_intent(data)

        return {
            "status": "OK",
            "intent": intent
        }

    except json.JSONDecodeError:
        return {
            "status": "LLM_INVALID_JSON",
            "raw": raw_text if 'raw_text' in locals() else "No response",
            "prompt_length": len(full_prompt) if 'full_prompt' in locals() else 0
        }

    except Exception as e:
        return {
            "status": "LLM_ERROR",
            "error": str(e),
            "prompt_length": len(full_prompt) if 'full_prompt' in locals() else 0
        }
