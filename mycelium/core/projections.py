LIVE_STATE = {
    "requests": {},
    "system": {},
}


def apply_live(event):

    t = event.get("type")
    p = event.get("payload", {})

    if not t:
        return

    if t == "acquisition.requested":
        LIVE_STATE["requests"][p["title"]] = "REQUESTED"

    elif t == "acquisition.available":
        LIVE_STATE["requests"][p["title"]] = "AVAILABLE"

    elif t == "acquisition.completed":
        LIVE_STATE["requests"][p["title"]] = "COMPLETED"

    elif t == "system.started":
        LIVE_STATE["system"]["started"] = True
