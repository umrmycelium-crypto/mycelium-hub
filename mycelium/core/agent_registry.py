from mycelium.core.agent import MyceliumAgent
from mycelium.runtime.media import media_play, media_search
from mycelium.runtime.developer import developer_handler
from mycelium.runtime.knowledge import knowledge_handler
from mycelium.runtime.system import system_status, system_deploy


def media_agent(payload, context):
    # Route to the specific media action based on the action in the payload
    # (This will be populated by the router/intent engine)
    action = payload.get("action", "media.play")

    if action == "media.search":
        return media_search(payload, context)
    return media_play(payload, context)


def system_agent(payload, context):
    # Route to the specific system action based on the action in the payload
    action = payload.get("action", "system.status")

    if action == "system.deploy":
        return system_deploy(payload, context)
    return system_status(payload, context)


def knowledge_agent(payload, context):
    return knowledge_handler(payload, context)


def developer_agent(payload, context):
    return developer_handler(payload, context)


AGENTS = {
    "media_agent": MyceliumAgent(
        name="media_agent",
        capabilities=["media.play", "media.search", "media.agent"],
        handler=media_agent
    ),

    "system_agent": MyceliumAgent(
        name="system_agent",
        capabilities=["system.status", "system.deploy"],
        handler=system_agent
    ),

    "knowledge_agent": MyceliumAgent(
        name="knowledge_agent",
        capabilities=["knowledge.search"],
        handler=knowledge_agent
    ),

    "developer_agent": MyceliumAgent(
        name="developer_agent",
        capabilities=["developer.assist"],
        handler=developer_agent
    ),
}


