import yaml
from typing import Optional, List, Dict, Any
from pathlib import Path
import os
from mycelium.llm.ollama_intent import llm_to_intent

class IntentRouter:
    """
    Routes natural language input to defined intents using semantic routing via the Local Brain (Ollama).
    """
    
    def __init__(self, intents_file: str = "mycelium/intents.yaml"):
        self.intents_file = intents_file

    def route(self, text: str) -> Dict[str, Any]:
        """
        Routes natural language input to a defined intent using the Local Brain.
        Returns a dictionary containing the intent and any extracted payload.
        """
        # Semantic Path: Local Brain (Ollama)
        llm_result = llm_to_intent(text)
        if llm_result["status"] == "OK":
            intent_data = llm_result["intent"]
            # The intent_data is expected to be the validated JSON from Ollama
            return {
                "intent": intent_data.get("intent"),
                "confidence": intent_data.get("confidence", 0.0),
                "payload": intent_data.get("payload", {}),
                "requires_confirmation": intent_data.get("requires_confirmation", False),
                "method": "semantic"
            }
        
        return {
            "intent": None,
            "confidence": 0.0,
            "payload": {},
            "requires_confirmation": True,
            "method": "none"
        }
