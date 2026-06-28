from mycelium.core.intent_router import IntentRouter
from mycelium.core.intent_registry import get_registry
from mycelium.core.intent_graph_executor import execute_graph
from typing import Dict, Any

class IntentEngine:
    """
    The main entry point for natural language command processing.
    """
    
    def __init__(self):
        self.router = IntentRouter()
        self.registry = get_registry()

    def process(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Takes raw text, routes it to an intent, and executes the handler.
        """
        context = context or {}
        intent_name = self.router.route(text)
        
        if not intent_name:
            return {
                "status": "UNKNOWN_INTENT",
                "input": text,
                "message": "I'm not sure how to handle that request yet."
            }
        
        handler = self.registry.get(intent_name)
        if not handler:
            return {
                "status": "NO_HANDLER",
                "intent": intent_name,
                "message": f"Intent {intent_name} recognized but no handler is implemented."
            }
        
        # Build the payload for the handler
        payload = {"input": text}
        
        try:
            result = handler(payload, context)
            return {
                "status": "SUCCESS",
                "intent": intent_name,
                "result": result
            }
        except Exception as e:
            return {
                "status": "EXECUTION_ERROR",
                "intent": intent_name,
                "error": str(e)
            }

# Singleton instance for easy access
engine = IntentEngine()
