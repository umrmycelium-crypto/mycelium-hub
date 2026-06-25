import json
from mycelium.core.cortex_schema import CortexDecision


class CognitiveCortex:

    def __init__(self, brain):
        self.brain = brain

    def evaluate(self, intent):

        # --- SIMPLE RULE LAYER (safe default) ---
        if intent.name == "system.ping":
            return CortexDecision(
                allow=True,
                signals=[{
                    "type": "system.ping",
                    "payload": intent.payload,
                    "context": intent.context
                }],
                reasoning="Direct system ping allowed"
            )

        # --- MEDIA EXPANSION LOGIC ---
        if intent.name == "media.play":

            title = intent.payload.get("title", "")

            return CortexDecision(
                allow=True,
                signals=[
                    {
                        "type": "media.search",
                        "payload": {"query": title},
                        "context": intent.context
                    },
                    {
                        "type": "media.play",
                        "payload": {"title": title},
                        "context": intent.context
                    }
                ],
                reasoning="Expanded play request into search + play pipeline"
            )

        # --- DEFAULT FALLBACK ---
        return CortexDecision(
            allow=True,
            signals=[{
                "type": intent.name,
                "payload": intent.payload,
                "context": intent.context
            }],
            reasoning="Pass-through execution"
        )
