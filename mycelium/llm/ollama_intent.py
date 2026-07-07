import json
import yaml
import requests
from pathlib import Path
from mycelium.core.intent_schema import validate_intent
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.models import get_llm_model, OLLAMA_URL

INTENTS_FILE = "mycelium/intents.yaml"


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


def llm_to_intent(user_text: str) -> dict:
    """
    Converts natural language → validated Intent object using dynamic prompt and cognitive context.
    """
    system_prompt = get_dynamic_system_prompt()
    cognitive_context = cognitive_state.get_snapshot()

    try:
        # We prime the LLM with the context before the user input
        full_prompt = f"{system_prompt}\n\nCognitive Context:\n{cognitive_context}\n\nUser input:\n{user_text}"
        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": get_llm_model(),
                "prompt": full_prompt,
                "stream": False
            },
            timeout=30
        )

        raw_text = response.json()["response"]

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
            "raw": raw_text if 'raw_text' in locals() else "No response"
        }

    except Exception as e:
        return {
            "status": "LLM_ERROR",
            "error": str(e)
        }
