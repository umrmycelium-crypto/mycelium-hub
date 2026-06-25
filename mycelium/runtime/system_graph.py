from mycelium.core.execution_trace import get_trace
from mycelium.core.registry_core import get_registry
from mycelium.core.secure_ledger import LEDGER

def build_graph():
    return {
        "nodes": [
            {"id": "event_bus", "type": "core"},
            {"id": "registry", "size": len(list(get_registry()))},
            {"id": "trace", "size": len(get_trace(50))},
            {"id": "ledger", "size": len(LEDGER)},
        ],
        "edges": [
            ["event_bus", "trace"],
            ["event_bus", "registry"],
            ["registry", "ledger"]
        ]
    }
