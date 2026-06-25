from mycelium.core.registry_core import get_registry

def load_handlers():
    """
    Explicit deterministic loading.
    NO circular imports.
    """

    import mycelium.core.handlers_system
    import mycelium.core.handlers_ai
    import mycelium.core.handlers_media


def validate_kernel():
    registry = get_registry()

    required = [
        "system.ping",
        "system.status",
        "ai.ask",
        "media.play"
    ]

    missing = [r for r in required if r not in registry]

    ok = len(missing) == 0
    return {"ok": ok, "missing": missing}


def bootstrap():
    load_handlers()

    validation = validate_kernel()

    if not validation["ok"]:
        raise RuntimeError(f"Kernel bootstrap failed: {validation['missing']}")

    return {
        "status": "BOOTSTRAPPED",
        "registry_size": len(get_registry().keys()),
        "ready": True
    }
