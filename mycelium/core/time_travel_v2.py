from mycelium.core.event_store_db import read_events


def replay_full():
    return read_events(1000)


def replay_range(start_ts: float, end_ts: float):
    events = read_events(2000)

    return [
        e for e in events
        if start_ts <= e["timestamp"] <= end_ts
    ]


def step_debug(n: int):
    return read_events(n)


def system_debug(payload, context):
    if "start" in payload:
        return replay_range(payload["start"], payload["end"])

    if "step" in payload:
        return step_debug(payload["step"])

    return replay_full()
