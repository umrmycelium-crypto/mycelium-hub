import yaml
from typing import Optional, List, Dict, Any
from pathlib import Path
import os

class IntentRouter:
    """
    Routes natural language input to defined intents using keyword matching 
    and falling back to LLM-based routing if available.
    """
    
    def __init__(self, intents_file: str = "mycelium/intents.yaml"):
        self.intents_file = intents_file
        self.intent_map = self._load_intents()

    def _load_intents(self) -> Dict[str, List[str]]:
        try:
            with open(self.intents_file, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading intents: {e}")
            return {}

    def route(self, text: str) -> Optional[str]:
        """
        Matches input text against keywords in intents.yaml.
        """
        text = text.lower().strip()
        
        # Simple keyword matching
        for intent, keywords in self.intent_map.items():
            for kw in keywords:
                if kw.lower() in text:
                    return intent
        
        return None

    def get_keywords_for_intent(self, intent: str) -> List[str]:
        return self.intent_map.get(intent, [])
