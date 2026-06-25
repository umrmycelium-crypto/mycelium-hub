import json
import requests
from mycelium.core.intent_schema import validate_intent


OLLAMA_URL = "http://localhost:11434/api/generate"


SYSTEM_PROMPT = """
You are an intent parser for the Mycelium system.

RULES:
- Output ONLY valid JSON
- No explanations
- No markdown
- No extra text

Return format:
{
  "intent": "...",
  "confidence": 0.0-1.0,
  "payload": {},
  "context": {},
  "requires_confirmation": false
}

Allowed intents:
- system.ping
- system.status
- media.play
- knowledge.search

If uncertain:
- use confidence < 0.6
- set requires_confirmation = true
"""


def llm_to_intent(user_text: str) -> dict:
    """
    Converts natural language → validated Intent object
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3.1",
                "prompt": SYSTEM_PROMPT + "\nUser input:\n" + user_text,
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
            "raw": raw_text
        }

    except Exception as e:
        return {
            "status": "LLM_ERROR",
            "error": str(e)
        }
