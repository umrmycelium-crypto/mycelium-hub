from typing import List, Dict, Any
from datetime import datetime

class ContextStore:
    """
    Tracks the short-term cognitive state of the system.
    Allows the Brain to resolve references (anaphora) and maintain continuity.
    """
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []
        self.last_intent: Dict[str, Any] = {}

    def add_event(self, event: Dict[str, Any]):
        """Adds a system event to short-term memory."""
        self.history.append(event)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def set_last_intent(self, intent: str, payload: Dict[str, Any]):
        """Remembers the last successfully executed intent."""
        self.last_intent = {
            "intent": intent,
            "payload": payload,
            "timestamp": datetime.now().isoformat()
        }

    def get_context_summary(self) -> str:
        """
        Returns a concise string representation of the current cognitive context.
        Used to prime the LLM for anaphora resolution.
        """
        if not self.history:
            return "No recent history."

        summary = "Recent System History:
"
        for i, event in enumerate(self.history):
            event_name = event.get("event", "unknown_event")
            payload = event.get("payload", {})
            summary += f"{i+1}. {event_name} | {payload}
"
        
        if self.last_intent:
            summary += f"
Last Action: {self.last_intent['intent']} ({self.last_intent['payload']})"
        
        return summary

# Singleton for system-wide context
context_store = ContextStore()
