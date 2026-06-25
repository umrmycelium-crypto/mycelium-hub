class CompilerMemory:
    def __init__(self):
        self.misses = []

    def record_miss(self, raw: str):
        self.misses.append(raw)


COMPILER_MEMORY = CompilerMemory()
