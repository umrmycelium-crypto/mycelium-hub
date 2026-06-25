from mycelium.core.bootstrap_kernel import bootstrap
from mycelium.core.registry_core import get_registry

def check():
    state = bootstrap()
    registry = get_registry()

    required = ["system.ping", "system.status", "ai.ask", "media.play"]

    missing = [r for r in required if r not in registry.keys()]

    return {
        "boot": state,
        "missing": missing,
        "stable": len(missing) == 0
    }

print(check())
