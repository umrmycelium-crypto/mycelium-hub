import asyncio
import math
import random


class Runtime:
    def __init__(self):
        self.tick = 0
        self.idea_counter = 0

        self.nodes = {
            "seed": {"activation": 0.5},
            "memory": {"activation": 0.2},
            "intent": {"activation": 0.7}
        }

        # persistent idea field
        self.ideas = [
            {
                "id": "idea_1",
                "name": "origin",
                "value": 0.5,
                "strength": 0.5,
                "phase": random.random(),
                "vec": [0.0, 0.0, 0.0]
            }
        ]

    def _idea_field(self):
        if not self.ideas:
            return 0.5
        return sum(i["value"] for i in self.ideas) / len(self.ideas)

    def step(self):
        self.tick += 1

        # -------------------------
        # NODE DYNAMICS
        # -------------------------
        for n in self.nodes:
            self.nodes[n]["activation"] *= 0.96

        # idea evolution: drift existing ideas instead of pure accumulation
        for idea in self.ideas:
            # emergent vector drift based on system fields
            idea["vec"][0] += (self.nodes["seed"]["activation"] - 0.5) * 0.01
            idea["vec"][1] += (self.nodes["memory"]["activation"] - 0.5) * 0.01
            idea["vec"][2] += (self.nodes["intent"]["activation"] - 0.5) * 0.01
            drift = (self.nodes["memory"]["activation"] - 0.1) * 0.01
            idea["strength"] = max(0.0, min(1.0, idea["strength"] + drift))

        # seed influences memory
        self.nodes["memory"]["activation"] += self.nodes["seed"]["activation"] * 0.01

        # intent becomes EMERGENT (not forced)
        idea_field = self._idea_field()
        self.nodes["intent"]["activation"] *= 0.98
        self.nodes["intent"]["activation"] += idea_field * 0.02

        # -------------------------
        # IDEA EVOLUTION (NOT BRANCHING)
        # -------------------------
        for i, idea in enumerate(self.ideas):
            drift = math.sin(self.tick * 0.01 + idea["phase"]) * 0.01

            # ideas influence each other via field
            field = idea_field - idea["value"]

            idea["value"] += drift + field * 0.02

            # clamp
            idea["value"] = max(0.01, min(1.0, idea["value"]))

        # -------------------------
        # SOFT IDEA STABILIZATION
        # -------------------------
        if self.tick % 30 == 0 and len(self.ideas) < 20:
            self.ideas.append({
                "id": f"idea_{self.tick}",
                "name": f"echo_{len(self.ideas)}",
                "value": random.uniform(0.3, 0.7),
                "strength": random.uniform(0.3, 0.7),
                "phase": random.random(),
                "vec": [0.0, 0.0, 0.0]
            })

        # generate evolving idea from intent coupling
        self.idea_counter += 1
        new_strength = self.nodes["intent"]["activation"] * 0.5 + self.nodes["seed"]["activation"] * 0.3
        if new_strength > 0.1:
            self.ideas.append({
                "id": f"idea_{self.idea_counter}",
                "name": f"idea_{self.idea_counter}",
                "value": new_strength,
                "strength": float(new_strength),
                "phase": random.random(),
                "vec": [0.0, 0.0, 0.0],
                "tick": self.tick
            })
        return {
            "tick": self.tick,
            "nodes": self.nodes,
            "ideas": self.ideas,
            "intent_field": idea_field
        }

    async def stream(self):
        while True:
            yield self.step()
            await asyncio.sleep(1)
