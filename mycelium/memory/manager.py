import json
from pathlib import Path
from datetime import datetime, timezone

# Persistent memory file path
MEMORY_FILE = Path("mycelium/memory/intent_memory.json")

def load_memory():
    """
    Loads the persistent intent memory store.
    """
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except Exception:
            pass
    return {"aliases": {}, "failed_intents": {}, "media.play": {}}

def save_memory(memory):
    """
    Saves the intent memory to disk.
    """
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

def record_success(intent, entity_value):
    """
    Records a successful intent resolution and entity mapping.
    """
    if not entity_value:
        return

    memory = load_memory()
    memory.setdefault(intent, {})
    
    entry = memory[intent].setdefault(str(entity_value), {
        "success_count": 0,
        "failure_count": 0,
        "last_used": None
    })

    entry["success_count"] += 1
    entry["last_used"] = datetime.now(timezone.utc).isoformat()

    save_memory(memory)

def record_failure(intent, original_text):
    """
    Records a failed intent resolution or execution.
    """
    memory = load_memory()
    memory.setdefault("failed_intents", {})
    
    memory["failed_intents"][original_text] = memory["failed_intents"].get(original_text, 0) + 1
    
    save_memory(memory)

def add_alias(alias, target_entity):
    """
    Manually or automatically adds a semantic alias.
    """
    memory = load_memory()
    memory["aliases"][alias.lower()] = target_entity
    save_memory(memory)
