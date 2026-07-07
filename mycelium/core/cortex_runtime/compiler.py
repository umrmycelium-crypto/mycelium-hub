import json

def build_prompt(user_input: str, registry_keys: list[str]) -> str:
    return f"""
You are the Mycelium Intent Compiler.

Convert input into STRICT JSON only.

RULES:
- Output ONLY valid JSON
- No commentary
- No extra keys
- Every intent must match registry exactly
- Confidence must be 0.0–1.0

Available intents:
{registry_keys}

Output format:
{{
  "version": "1.0",
  "intents": [
    {{
      "name": "string",
      "confidence": float,
      "payload": {{}}
    }}
  ],
  "meta": {{
    "needs_clarification": false
  }}
}}

User input:
\"\"\"{user_input}\"\"\"
"""
