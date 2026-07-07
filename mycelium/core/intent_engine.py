from mycelium.core.intent_router import IntentRouter
from mycelium.core.dispatcher import dispatcher
from typing import Dict, Any

class IntentEngine:
    """
    The main entry point for natural language command processing.
    """
    
    def __init__(self):
        self.router = IntentRouter()

    def process(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Takes raw text, routes it to an intent, and executes the handler via the dispatcher.
        """
        context = context or {}
        
        # --- GALAXY WOLF SOVEREIGN FAST-PASS ---
        # We use a case-insensitive check to ensure maximum reliability for the wake-word.
        if text.lower().startswith("galaxy wolf"):
            from mycelium.core.agent_registry import AGENTS
            miliana_agent = AGENTS.get("miliana_core")
            if miliana_agent:
                # Remove wake-word and punctuation for cleaner agent processing
                clean_text = text.replace("Galaxy Wolf!", "").replace("Galaxy Wolf", "").strip()
                
                # Direct execution via the agent's ReAct loop
                result = miliana_agent.run(clean_text)
                
                return {
                    "status": "SUCCESS",
                    "intent": "sovereign.miliana",
                    "result": result,
                    "method": "sovereign_fast_pass"
                }
        
        routing_result = self.router.route(text)
        
        intent_name = routing_result.get("intent")
        payload = routing_result.get("payload")
        requires_confirmation = routing_result.get("requires_confirmation", False)
        
        if not intent_name:
            return {
                "status": "UNKNOWN_INTENT",
                "input": text,
                "message": "I'm not sure how to handle that request yet."
            }
        
        if requires_confirmation:
            return {
                "status": "REQUIRES_CONFIRMATION",
                "intent": intent_name,
                "payload": payload,
                "message": f"I think you want to {intent_name}, is that correct?"
            }
        
        try:
            # Route the intent through the dispatcher for pipeline expansion and execution
            dispatch_result = dispatcher.dispatch(intent_name, payload, context)
            
            if dispatch_result["status"] == "SUCCESS":
                return {
                    "status": "SUCCESS",
                    "intent": intent_name,
                    "result": dispatch_result["final_result"],
                    "method": routing_result.get("method")
                }
            else:
                return {
                    "status": "EXECUTION_ERROR",
                    "intent": intent_name,
                    "message": f"Dispatcher error: {dispatch_result.get('reasoning')}",
                    "details": dispatch_result
                }
                
        except Exception as e:
            return {
                "status": "EXECUTION_ERROR",
                "intent": intent_name,
                "error": str(e)
            }

# Singleton instance for easy access
engine = IntentEngine()
