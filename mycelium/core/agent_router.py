from mycelium.core.agent_registry import AGENTS


class AgentRouter:

    @staticmethod
    def resolve(intent_name: str):

        for agent in AGENTS.values():
            if intent_name in agent.capabilities:
                return agent

        return None
