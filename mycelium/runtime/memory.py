from mycelium.core.event_store import read_events


def build_memory(limit: int = 20):
    """
    Convert event history into semantic AI context.
    Synthesizes raw events into a narrative that the AI can use to understand state.
    """

    events = read_events()[-limit:]
    if not events:
        return "The system memory is currently empty."

    memory_lines = []

    for i, e in enumerate(events):
        etype = e.get("type", "unknown")
        payload = e.get("payload", {})
        
        # Extract common fields regardless of event type
        source = payload.get("source", "system")
        title = payload.get("title", "")
        
        if etype == "user.presence":
            status = payload.get("status", "unknown")
            desc = f"Event {i}: User presence ({source}) detected as {status}"
        elif etype == "intent.executed":
            intent = payload.get("intent", "unknown")
            desc = f"Event {i}: Successfully executed '{intent}'"
        elif etype == "intent.unhandled":
            raw = payload.get("payload", {}).get("raw", "unknown")
            desc = f"Event {i}: Unhandled input from {source}: '{raw}'"
        elif "voice" in etype or "audio" in etype:
            desc = f"Event {i}: Voice activity from {source}"
        elif etype == "unknown" or not etype:
            if title:
                desc = f"Event {i}: Activity related to '{title}' from {source}"
            elif source != "system":
                desc = f"Event {i}: Generic activity from {source}"
            else:
                desc = f"Event {i}: Internal system event {payload}"
        else:
            desc = f"Event {i}: {etype} from {source}: {payload}"
        
        memory_lines.append(desc)

    return "\n".join(memory_lines)
