def system_ping(payload=None):
    return {
        "status": "OK",
        "message": "pong",
        "source": "system.ping"
    }


REGISTRY = {
    "system.ping": system_ping,
}
