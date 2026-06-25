import asyncio
from mycelium.core.self_model import build_self_state
from mycelium.core.event_hooks import emit


async def self_loop():
    while True:
        await asyncio.sleep(1)

        state = build_self_state()

        emit("system.self", state)
