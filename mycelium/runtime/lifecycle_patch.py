import asyncio
from mycelium.core.self_loop import self_loop


async def start_self_model():
    asyncio.create_task(self_loop())
