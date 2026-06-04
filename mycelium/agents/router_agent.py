import json
import subprocess

# System prompt to enforce structured output
SYSTEM_PROMPT = """
You are a high-precision intent routing system for the Mycelium Ecosystem.
Your task is to classify user requests into one of the following intents and extract entities.

Valid intents:
- media.play: User wants to watch or play a specific movie/show.
- media.search: User wants to find or look up media.
- system.status: User asks about the health or status of the system/services.
- knowledge.search: User wants to search their notes, vault, or knowledge base.
- developer.assist: User wants technical analysis or help with the codebase.
- unknown: Use if the request does not fit any category.

Rules:
1. Return ONLY valid JSON matching the schema below.
2. No conversational text, no explanations, no preamble.
3. For media.play, put the title in entities.title.
4. For searches, put the search term in entities.query.

Schema:
{
  "intent": "intent.name",
  "confidence": 0.0-1.0,
  "entities": {
    "title": "extracted title",
    "query": "extracted query"
  }
}
"""

def route_intent(text: str):
    """
    Interfaces with Ollama (Llama 3.1) to classify natural language intent.
    """
    # Using llama3.1:latest as it's available on the host
    cmd = [
        "ollama",
        "run",
        "llama3.1:latest",
        f"{SYSTEM_PROMPT}\n\nInput: \"{text}\""
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Extract JSON from response (handling potential markdown formatting)
        output = result.stdout.strip()
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "{" in output:
            output = output[output.find("{"):output.rfind("}")+1]

        data = json.loads(output)
        return data
    except Exception as e:
        # Fallback to unknown if LLM fails
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "entities": {"error": str(e)}
        }
