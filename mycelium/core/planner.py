from mycelium.core.agent_router import AgentRouter


class ExecutionPlan:

    def __init__(self):
        self.steps = []


class Planner:

    @staticmethod
    def build(intent):

        agent = AgentRouter.resolve(intent.name)

        if not agent:
            return ExecutionPlan()

        plan = ExecutionPlan()
        plan.steps.append({
            "agent": agent,
            "intent": intent
        })

        return plan
