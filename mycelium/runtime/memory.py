from mycelium.core.event_store import read_events


def build_memory(limit: int = 20):
    """
    Convert event history into compact AI context
    """

    events = read_events()[-limit:]

    memory_lines = []

    for e in events:
        t = e.get("type", "unknown")
        payload = e.get("payload", {})

        memory_lines.append(f"- {t}: {payload}")

    return "\n".join(memory_lines)
