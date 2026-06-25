from mycelium.core.agent import Agent
from mycelium.runtime.media import media_play


def media_agent(payload, context):
    return media_play(payload, context)


def system_agent(payload, context):
    return {"status": "OK", "system": "healthy"}


AGENTS = {
    "media_agent": Agent(
        name="media_agent",
        capabilities=["media.play", "media.search"],
        handler=media_agent
    ),

    "system_agent": Agent(
        name="system_agent",
        capabilities=["system.ping", "system.status"],
        handler=system_agent
    ),
}
