class WeightedVote:
    def __init__(self, agent, vote, weight, reason=""):
        self.agent = agent
        self.vote = vote  # YES / NO / ABSTAIN
        self.weight = weight
        self.reason = reason

    def to_dict(self):
        return {
            "agent": self.agent,
            "vote": self.vote,
            "weight": self.weight,
            "reason": self.reason
        }
