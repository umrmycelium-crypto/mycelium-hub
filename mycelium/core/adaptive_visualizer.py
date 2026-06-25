from mycelium.core.execution_trace import get_trace


def compute_focus_area():
    trace = get_trace(200)

    intent_counts = {}

    for t in trace:
        intent = t.get("data", {}).get("intent", "unknown")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    if not intent_counts:
        return "idle"

    return max(intent_counts, key=intent_counts.get)


def system_adaptive_view(payload, context):
    return {
        "focus": compute_focus_area(),
        "trace_sample": get_trace(20),
        "mode": "auto-optimized-observability"
    }
