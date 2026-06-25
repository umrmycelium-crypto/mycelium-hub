from mycelium.runtime.registry import REGISTRY
from mycelium.core.validator import IntentValidator


def run(intent):

    intent = IntentValidator.validate(intent)

    handler = REGISTRY.get(intent.name)

    if not handler:
        return {
            "status": "NO_HANDLER",
            "intent": intent.name
        }

    return handler(intent.payload, intent.context)

# --- Mycelium acquisition worker wiring ---
from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.acquisition_worker import handle_acquisition

EVENT_BUS.subscribe(handle_acquisition)
