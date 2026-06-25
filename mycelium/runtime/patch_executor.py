import os
from mycelium.core.event_bus import EVENT_BUS


ALLOWED_ROOTS = [
    "mycelium/core/",
    "mycelium/runtime/",
    "mshell.py"
]


def is_allowed(path: str) -> bool:
    return any(path.startswith(root) for root in ALLOWED_ROOTS)


def apply_patch(patch: dict):
    """
    patch format:
    {
        "action": "patch",
        "path": "...",
        "content": "..."
    }
    """

    path = patch.get("path")
    content = patch.get("content")

    if not path or content is None:
        return {
            "status": "ERROR",
            "message": "Invalid patch format"
        }

    if not is_allowed(path):
        return {
            "status": "REJECTED",
            "message": f"Path not allowed: {path}"
        }

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        EVENT_BUS.publish({
            "type": "system.patch.applied",
            "payload": {
                "path": path
            }
        })

        return {
            "status": "OK",
            "message": "Patch applied",
            "path": path
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
