from mycelium.core.registry import REGISTRY  # IMPORTANT: forces decorator execution


REQUIRED = [
    "system.ping",
    "system.status",
    "system.events",
    "system.drift",
    "ai.ask",
    "media.play",
]


def bootstrap():
    missing = [k for k in REQUIRED if k not in REGISTRY]

    if missing:
        raise RuntimeError(f"Bootstrap failed. Missing handlers: {missing}")

    return {
        "status": "BOOTSTRAPPED",
        "registry_size": len(REGISTRY),
        "ready": True
    }
