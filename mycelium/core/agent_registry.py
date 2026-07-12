from mycelium.core.agent_base import BaseAgent
from mycelium.agents.creative_cores import MagnusCore, MilianaCore
from mycelium.agents.executive_agent import executive_agent_personal, executive_agent_public
from mycelium.runtime.media import media_play, media_search
from mycelium.runtime.developer import developer_handler
from mycelium.runtime.knowledge import knowledge_handler
from mycelium.runtime.system import system_status, system_deploy

class MyceliumAgent:
    """
    A simple wrapper to maintain compatibility between functional handlers 
    and autonomous agent classes.
    """
    def __init__(self, name, capabilities, handler):
        self.name = name
        self.capabilities = capabilities
        self.handler = handler

    def run(self, task_input):
        return self.handler(task_input, {})

AGENTS = {
    "executive_agent": MyceliumAgent(
        name="executive_agent",
        capabilities=["system.exec", "system.file", "system.mesh"],
        handler=lambda x: executive_agent_personal.run(x)
    ),
    "executive_agent_public": MyceliumAgent(
        name="executive_agent_public",
        capabilities=["system.exec", "system.file", "system.mesh"],
        handler=lambda x: executive_agent_public.run(x)
    ),
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
        handler=knowledge_handler
    ),

    "developer_agent": MyceliumAgent(
        name="developer_agent",
        capabilities=["developer.assist"],
        handler=developer_handler
    ),

    "magnus_core": MagnusCore(),
    "miliana_core": MilianaCore(),
}
