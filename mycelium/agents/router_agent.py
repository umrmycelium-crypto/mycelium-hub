import json
import subprocess
import yaml
import os

# Path to intents file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Moving up two levels from mycelium/agents/ to mycelium/ to find intents.yaml
INTENTS_PATH = os.path.join(BASE_DIR, "..", "..", "intents.yaml")

def get_dynamic_system_prompt():
    """
    Loads intents from YAML and constructs a high-precision system prompt.
    """
    try:
        with open(INTENTS_PATH, "r") as f:
            intents = yaml.safe_load(f)
    except Exception:
        intents = {}

    intents_description = ""
    for intent, keywords in intents.items():
        keyword_str = ", ".join(keywords)
        intents_description += f"- {intent} (associated keywords: {keyword_str})\n"

    return f"""
You are a high-precision intent routing system for the Mycelium Ecosystem.
Your task is to classify user requests into one of the following intents and extract entities.

Valid intents:
{intents_description}
- unknown: Use if the request does not fit any category.

Rules:
1. Return ONLY valid JSON matching the schema below.
2. No conversational text, no explanations, no preamble.
3. For media.play, put the title in entities.title.
4. For searches, put the search term in entities.query.

Schema:
{{
  "intent": "intent.name",
  "confidence": 0.0-1.0,
  "entities": {{
    "title": "extracted title",
    "query": "extracted query"
  }}
}}
"""

def route_intent(text: str):
    """
    Interfaces with Ollama (Llama 3.1) to classify natural language intent.
    """
    system_prompt = get_dynamic_system_prompt()
    
    # Using llama3.1:latest as it's available on the host
    cmd = [
        "ollama",
        "run",
        "llama3.1:latest",
        f"{system_prompt}\n\nInput: \"{text}\""
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
