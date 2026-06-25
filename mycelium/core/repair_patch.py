class Patch:
    def __init__(self, target, change, reason):
        self.target = target
        self.change = change
        self.reason = reason
        self.applied = False

    def to_dict(self):
        return {
            "target": self.target,
            "change": self.change,
            "reason": self.reason,
            "applied": self.applied
        }
