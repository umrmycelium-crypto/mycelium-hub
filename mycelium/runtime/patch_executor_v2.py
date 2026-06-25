import os
from mycelium.core.event_bus import EVENT_BUS


ALLOWED_ROOTS = [
    "mycelium/core/",
    "mycelium/runtime/",
    "mshell.py"
]


def is_allowed(path):
    return any(path.startswith(r) for r in ALLOWED_ROOTS)


def apply_patch_safe(patch):
    """
    patch = {
        "path": "...",
        "content": "...",
        "auto_apply": bool
    }
    """

    path = patch.get("path")
    content = patch.get("content")

    if not path or content is None:
        return {"status": "ERROR", "message": "invalid patch"}

    if not is_allowed(path):
        return {"status": "REJECTED", "message": "unsafe path"}

    # AUTO APPLY ONLY IF FLAGGED
    if not patch.get("auto_apply", False):
        EVENT_BUS.publish({
            "type": "system.repair.pending",
            "payload": patch
        })
        return {"status": "PENDING_REVIEW"}

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    EVENT_BUS.publish({
        "type": "system.repair.applied",
        "payload": patch
    })

    return {"status": "APPLIED", "path": path}
