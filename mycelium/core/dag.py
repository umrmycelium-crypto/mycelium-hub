class DAGNode:
    def __init__(self, intent):
        self.intent = intent  # stored, but NEVER assumed as object behavior

    def execute(self, kernel):
        return kernel(self.intent)
