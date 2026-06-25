from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.event_store import read_events


MAX_RETRIES = 2


def get_attempt_count(title):
    events = read_events()
    return sum(
        1 for e in events
        if e.get("type") == "acquisition.requested"
        and e.get("payload", {}).get("title") == title
    )


def handle_acquisition(event):
    payload = event.get("payload", {})
    title = payload.get("title")

    if not title:
        return

    attempts = get_attempt_count(title)

    if attempts > MAX_RETRIES:
        EVENT_BUS.publish({
            "type": "acquisition.failed",
            "payload": {
                "title": title,
                "reason": "max_retries_exceeded"
            }
        })
        return

    # simulate retry lifecycle
    EVENT_BUS.publish({
        "type": "acquisition.retrying",
        "payload": {
            "title": title,
            "attempt": attempts
        }
    })

    # re-dispatch acquisition request (controlled loop)
    EVENT_BUS.publish({
        "type": "acquisition.requested",
        "payload": {
            "title": title
        }
    })
