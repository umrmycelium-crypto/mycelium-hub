class Brain:

    def __init__(self):
        self.state = {
            "facts": {},
            "last_actions": [],
            "agent_memory": {}
        }

    def update(self, key, value):
        self.state[key] = value

    def append(self, key, value):
        if key not in self.state:
            self.state[key] = []
        self.state[key].append(value)

    def get(self):
        return self.state
