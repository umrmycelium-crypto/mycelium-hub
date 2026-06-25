from mycelium.core.event_store import read_events


def get_repair_status():
    events = read_events()

    failures = [e for e in events if e.get("type") in ("intent.failed", "acquisition.failed")]
    repairs = [e for e in events if e.get("type") == "system.repair.suggested"]
    applied = [e for e in events if e.get("type") == "system.repair.applied"]

    return {
        "failures": len(failures),
        "suggestions": len(repairs),
        "applied": len(applied),
        "recent_failures": failures[-5:],
        "recent_repairs": repairs[-5:]
    }
