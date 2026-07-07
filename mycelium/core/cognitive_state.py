import json
import os
from collections import deque
from typing import Any, Dict, List, Optional
from datetime import datetime
from mycelium.knowledge import search_notes

class CognitiveState:
    """
    Unified Cognitive State Manager for the Mycelium Ecosystem.
    Integrates working memory, persistent facts, and long-term knowledge retrieval.
    """
    def __init__(self, state_file: str = "state/cognitive_state.json", max_history: int = 15):
        self.state_file = state_file
        self.max_history = max_history
        
        # Working Memory: Short-term sliding window of system events
        self.working_memory = deque(maxlen=max_history)
        
        # Active Focus: The current primary entity/topic of interaction
        self.active_focus: Optional[Dict[str, Any]] = None
        
        # Fact Store: Persistent mid-term memory
        self.fact_store: Dict[str, Any] = self._load_facts()

    def _load_facts(self) -> Dict[str, Any]:
        """Loads persistent facts from the JSON state file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading fact store: {e}")
        return {}

    def _save_facts(self):
        """Saves the current fact store to the JSON state file."""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.fact_store, f, indent=4)
        except IOError as e:
            print(f"Error saving fact store: {e}")

    def update_fact(self, key: str, value: Any):
        """Updates a persistent fact and saves it to disk."""
        self.fact_store[key] = value
        self._save_facts()

    def get_fact(self, key: str, default: Any = None) -> Any:
        """Retrieves a persistent fact."""
        return self.fact_store.get(key, default)

    def add_event(self, event_name: str, payload: Dict[str, Any]):
        """Records a system event in working memory."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "payload": payload
        }
        self.working_memory.append(event)

    def set_focus(self, entity_type: str, entity_id: str, metadata: Optional[Dict[str, Any]] = None):
        """Sets the current primary entity for anaphora resolution."""
        self.active_focus = {
            "type": entity_type,
            "id": entity_id,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        # Also record this as an event in working memory
        self.add_event("focus_shift", {"entity": entity_id, "type": entity_type})

    def query_knowledge(self, query: str) -> List[str]:
        """Interfaces with mycelium.knowledge to retrieve relevant notes."""
        return search_notes(query)

    def get_snapshot(self) -> str:
        """
        Generates a comprehensive text summary of the current cognitive state.
        Used to prime the LLM for context-aware intent parsing.
        """
        lines = []
        
        # 1. Active Focus
        if self.active_focus:
            lines.append(f"Current Focus: {self.active_focus['type']} '{self.active_focus['id']}'")
        else:
            lines.append("Current Focus: None")

        # 2. Working Memory
        lines.append("\nRecent System History:")
        if not self.working_memory:
            lines.append("- No recent events.")
        else:
            for i, event in enumerate(self.working_memory):
                lines.append(f"{i+1}. {event['event']} | {event['payload']}")

        # 3. Relevant Facts
        lines.append("\nRelevant Persistent Facts:")
        if not self.fact_store:
            lines.append("- No stored facts.")
        else:
            for key, value in self.fact_store.items():
                lines.append(f"- {key}: {value}")

        return "\n".join(lines)

# Singleton for system-wide access
cognitive_state = CognitiveState()
