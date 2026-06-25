import time
from mycelium.core.execution_trace import get_trace
from mycelium.core.registry_core import get_registry
from mycelium.core.secure_ledger import LEDGER


def build_self_state():
    reg = get_registry()

    return {
        "ts": time.time(),
        "trace_len": len(get_trace(100)),
        "registry_size": len(reg) if hasattr(reg, "__len__") else len(list(reg)),
        "ledger_size": len(LEDGER),
        "identity": "mycelium.runtime.core",
    }
