import json
import subprocess

# System prompt for multi-intent decomposition
SYSTEM_PROMPT = """
You are a task decomposition engine for the Mycelium Ecosystem.
Your job is to convert a single user input into a JSON list of independent, ordered actions.

Valid intents:
- media.play: Watch or play a specific movie/show.
- media.search: Find or look up media.
- system.status: Check health or status of the system/services.
- knowledge.search: Search notes, vault, or knowledge base.
- developer.assist: Technical analysis or codebase help.

Return ONLY a valid JSON list in this format:
[
  {
    "intent": "intent.name",
    "entities": {
      "title": "extracted title",
      "query": "extracted query"
    }
  }
]

Rules:
1. Split ALL distinct actions (e.g., "play X and search Y" becomes two entries).
2. Maintain the original order of execution.
3. No conversational text, no explanations, no preamble.
4. If only one action exists, return a single-item list.
5. If an action is unknown, use intent "unknown".
"""

def decompose(text: str, context: dict = None):
    """
    Interfaces with Ollama (Llama 3.1) to decompose complex requests into an event list,
    aware of current system state and recent history.
    """
    
    context_block = ""
    if context:
        # Format recent events for the prompt
        history = "\n".join([f"- {e.get('event')}: {e.get('payload', {}).get('text', '')}" for e in context.get("recent_events", [])])
        
        # Format relevant memory (simplified for prompt efficiency)
        memory = context.get("memory", {})
        memory_summary = f"Aliases: {memory.get('aliases')}\nFailed Phrases: {list(memory.get('failed_intents', {}).keys())}"

        context_block = f"""
SYSTEM STATE:
{context.get('state', 'Unknown')}

RECENT HISTORY:
{history}

PERSISTENT MEMORY (Success Patterns):
{memory_summary}
"""

    prompt = f"""
{SYSTEM_PROMPT}

{context_block}

USER INPUT:
"{text}"
"""

    cmd = [
        "ollama",
        "run",
        "llama3.1:latest",
        prompt
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Extract JSON list from response
        output = result.stdout.strip()
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "[" in output:
            output = output[output.find("["):output.rfind("]")+1]

        events = json.loads(output)
        if not isinstance(events, list):
            events = [events]
        return events
    except Exception as e:
        # Fallback to single 'unknown' event if LLM fails
        return [
            {
                "intent": "unknown",
                "entities": {"error": str(e), "text": text}
            }
        ]
