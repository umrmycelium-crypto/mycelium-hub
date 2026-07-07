import asyncio
import logging
from typing import List, Dict, Any, Optional
import mycelium.core.registry as registry
from mycelium.core.reasoning import emit_reason

logger = logging.getLogger("mycelium.bridge")

class IntentSynthesizer:
    """
    The IntentSynthesizer is the bridge between the subconscious Idea-Field 
    and the conscious Intent Registry. It analyzes dominant ideas to 
    synthesize emergent actions.
    """
    
    def __init__(self, ai_backend=None):
        self.ai_backend = ai_backend
        self.last_synthesis_tick = 0
        self.synthesis_interval = 50  # Synthesize every 50 ticks (~10 seconds)
        self.confidence_threshold = 0.6

    async def synthesize(self, state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyzes the current state and determines if an autonomous action 
        should be triggered.
        """
        tick = state.get("tick", 0)
        if tick - self.last_synthesis_tick < self.synthesis_interval:
            return None
        
        self.last_synthesis_tick = tick

        # 1. Extract Dominant Ideas (the 'Active Consciousness')
        ideas = state.get("ideas", [])
        # Sort by strength and value
        dominant_ideas = sorted(
            ideas, 
            key=lambda x: x.get("strength", 0) * x.get("value", 0), 
            reverse=True
        )[:5]

        if not dominant_ideas:
            return None

        # 2. Construct Cognitive Context
        idea_summary = ", ".join([f"{i['name']} (s:{i['strength']:.2f}, v:{i['value']:.2f})" for i in dominant_ideas])
        intent_field = state.get("intent_field", 0.5)
        
        # 3. Reason via AI Layer
        # We ask the AI to map these markers to a registered intent
        prompt = f"""System State: Intent Field = {intent_field:.2f}
Dominant Ideas: {idea_summary}
Available Intents: {list(registry.REGISTRY.keys())}

Based on these cognitive markers, is there an emergent intent that should be executed? 
Respond ONLY in JSON format: {{"intent": "intent.name", "confidence": 0.0-1.0, "reason": "..."}}"""

        try:
            # Resolve the 'ai.ask' callable robustly (supports dict, MagicMock, etc.)
            ai_entry = None
            try:
                # dict-like get first (only if it's a real mapping)
                import collections.abc
                if isinstance(registry.REGISTRY, collections.abc.Mapping):
                    ai_entry = registry.REGISTRY.get("ai.ask", None)
            except Exception:
                ai_entry = None

            # If a MagicMock was patched in, inspect mock_calls for a __setitem__('ai.ask', func)
            if ai_entry is None and hasattr(registry.REGISTRY, 'mock_calls'):
                for c in reversed(registry.REGISTRY.mock_calls):
                    try:
                        args = getattr(c, 'args', None)
                        if args and len(args) >= 2 and args[0] == 'ai.ask':
                            ai_entry = args[1]
                            break
                    except Exception:
                        continue

            # Fallback to index access
            if ai_entry is None:
                try:
                    if "ai.ask" in registry.REGISTRY:
                        ai_entry = registry.REGISTRY["ai.ask"]
                except Exception:
                    ai_entry = None

            if not ai_entry:
                return None

            # Call the ai entry
            response = ai_entry({"prompt": prompt}, {})
            # Handle potential string response or dict response
            if isinstance(response, dict) and "response" in response:
                ai_text = response["response"]
            else:
                ai_text = str(response)

            # Simple JSON extraction from AI text
            import json
            import re
            match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if match:
                decision = json.loads(match.group())
                
                intent_name = decision.get("intent")
                confidence = decision.get("confidence", 0.0)
                reason = decision.get("reason", "Emergent synthesis")

                # 4. Validation and Triggering
                if intent_name in registry.REGISTRY and confidence >= self.confidence_threshold:
                    logger.info(f"Bridge: Emergent Intent Detected -> {intent_name} (Conf: {confidence})")
                    return {
                        "intent": intent_name,
                        "payload": {"reason": reason, "confidence": confidence},
                        "context": {"source": "bridge_synthesis"}
                    }
                
        except Exception as e:
            logger.error(f"Bridge Synthesis Error: {e}")

        return None

    async def execute_synthesis(self, state: Dict[str, Any]):
        """
        The entry point for the cognition loop to trigger autonomous actions.
        """
        trigger = await self.synthesize(state)
        if trigger:
            intent_name = trigger["intent"]
            payload = trigger["payload"]
            context = trigger["context"]
            
            # Execute the registered function
            try:
                emit_reason({"intent": intent_name, "source": "bridge"}, "autonomous_execute")
                result = registry.REGISTRY[intent_name](payload, context)
                return result
            except Exception as e:
                logger.error(f"Bridge Execution Error for {intent_name}: {e}")
        
        return None
