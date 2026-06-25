import json
from mycelium.core.governance_timeline import build_timeline


def export_timeline_json(limit=200, path="timeline.json"):
    timeline = build_timeline(limit)

    with open(path, "w") as f:
        json.dump(timeline, f, indent=2)

    return {
        "status": "exported",
        "path": path,
        "count": len(timeline)
    }
