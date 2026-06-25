import time

AUDIT_LOG = []


def log_governance_event(event_type, payload):
    AUDIT_LOG.append({
        "timestamp": time.time(),
        "event": event_type,
        "payload": payload
    })


def get_audit(limit=100):
    return AUDIT_LOG[-limit:]
