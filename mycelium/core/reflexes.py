from mycelium.core.nervous_bus import NervousBus


class ReflexEngine:

    def __init__(self, bus: NervousBus, brain):
        self.bus = bus
        self.brain = brain

    def register_reflex(self, signal_type, agent):

        def handler(signal):
            return agent.act(signal, self.brain)

        self.bus.subscribe(signal_type, handler)
