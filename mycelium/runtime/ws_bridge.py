clients = set()

async def register_client(ws):
    clients.add(ws)

async def unregister_client(ws):
    clients.discard(ws)

async def broadcast(message):
    dead = []

    for ws in list(clients):
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)

    for ws in dead:
        clients.discard(ws)
