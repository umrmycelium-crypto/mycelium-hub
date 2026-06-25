from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.execution_trace import get_trace
from mycelium.core.registry_core import get_registry

def emit_self_observation():
    snapshot = {
        "intent": "system.self.observe",
        "trace": get_trace(20),
        "registry_size": len(list(get_registry())),
    }

    EVENT_BUS.emit("system.self.observe", snapshot)
    return snapshot
