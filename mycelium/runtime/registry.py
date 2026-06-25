def system_ping(payload, context):
    return {
        "status": "OK",
        "message": "pong"
    }


def system_status(payload, context):
    return {
        "status": "OK",
        "uptime": "unknown",
        "services": ["runtime"]
    }


REGISTRY = {
    "system.ping": system_ping,
    "system.status": system_status,
}
from mycelium.runtime.media import media_play

REGISTRY = {
    "system.ping": system_ping,
    "system.status": system_status,
    "media.play": media_play,
}
