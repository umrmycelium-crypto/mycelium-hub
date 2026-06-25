from mycelium.core.planner import Planner


class Executor:

    @staticmethod
    def execute(intent):

        plan = Planner.build(intent)

        results = []

        for step in plan.steps:

            agent = step["agent"]
            intent = step["intent"]

            result = agent.handler(intent.payload, intent.context)

            results.append({
                "agent": agent.name,
                "result": result
            })

        return results
