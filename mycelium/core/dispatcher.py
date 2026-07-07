from typing import Dict, Any, List, Callable
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.cortex import CognitiveCortex




from mycelium.agents.media_agent import media_agent
from mycelium.agents.knowledge_agent import knowledge_agent
from mycelium.agents.development_agent import development_agent
from mycelium.agents.system_agent import system_agent

class IntentDispatcher:
    """
    The 'Hand' of the system. Routes processed intents to functional handlers,
    coordinates action pipelines, and updates the cognitive state.
    """
    def __init__(self):
        # Integration with the Cortex for simple intent expansion
        self.cortex = CognitiveCortex(cognitive_state)
        self.handlers: Dict[str, Callable] = {}

    def register_handler(self, intent_name: str, handler: Callable):
        """Binds an intent name to a Python function."""
        self.handlers[intent_name] = handler

    def dispatch(self, intent_name: str, payload: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executes an intent. Routes specialized intents to autonomous agents.
        """
        context = context or {}
        
        # 1. Agent Routing Map
        agent_map = {
            "media": media_agent,
            "knowledge": knowledge_agent,
            "developer": development_agent,
            "system": system_agent
        }
        
        # Identify if the intent belongs to an agent (e.g., "media.play" -> "media")
        agent_key = intent_name.split(".")[0]
        if agent_key in agent_map:
            agent = agent_map[agent_key]
            # Extract the query or title from payload for the agent
            task_input = payload.get("title") or payload.get("query") or payload.get("input") or intent_name
            result = agent.run(task_input)
            return {
                "status": "SUCCESS",
                "pipeline": [{"agent": agent.name, "result": result}],
                "final_result": result,
                "reasoning": f"Handled autonomously by {agent.name}"
            }

        # 2. Cortex Evaluation: Expand simple non-agent intents into a set of signals
        class IntentObj:
            def __init__(self, name, payload, context):
                self.name = name
                self.payload = payload
                self.context = context

        decision = self.cortex.evaluate(IntentObj(intent_name, payload, context))
        
        if not decision.allow:
            return {"status": "DENIED", "reason": decision.reasoning}

        # 3. Signal Execution Pipeline
        results = []
        for signal in decision.signals:
            sig_type = signal["type"]
            sig_payload = signal["payload"]
            
            cognitive_state.add_event(f"executing_{sig_type}", sig_payload)
            
            handler = self.handlers.get(sig_type)
            if not handler:
                results.append({"signal": sig_type, "status": "NO_HANDLER"})
                continue
                
            try:
                res = handler(sig_payload, context)
                results.append({"signal": sig_type, "status": "SUCCESS", "result": res})
                
                if isinstance(res, dict) and "entity_id" in res:
                    entity_type = res.get("entity_type", "unknown")
                    cognitive_state.set_focus(entity_type, res["entity_id"], res.get("metadata"))
                    
            except Exception as e:
                results.append({"signal": sig_type, "status": "ERROR", "error": str(e)})

        return {
            "status": "SUCCESS" if len(results) > 0 and results[-1]["status"] == "SUCCESS" else "PARTIAL_FAILURE",
            "pipeline": results,
            "final_result": results[-1]["result"] if results else None,
            "reasoning": decision.reasoning
        }

# Singleton instance
dispatcher = IntentDispatcher()
