from mycelium.core.event_store import read_events


def replay_range(start: float, end: float):
    events = read_events()

    snapshot = []

    for e in events:
        t = e.get("timestamp", 0)
        if start <= t <= end:
            snapshot.append(e)

    return {
        "start": start,
        "end": end,
        "events": snapshot
    }


def replay_step(index: int):
    events = read_events()
    return events[:index]


def system_time_travel(payload, context):
    if "start" in payload and "end" in payload:
        return replay_range(payload["start"], payload["end"])

    return replay_step(payload.get("index", 10))
