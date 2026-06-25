class ConstitutionalVote:
    def __init__(self, agent, proposal_id, vote, reason=""):
        self.agent = agent
        self.proposal_id = proposal_id
        self.vote = vote  # YES / NO / ABSTAIN
        self.reason = reason

    def to_dict(self):
        return {
            "agent": self.agent,
            "proposal_id": self.proposal_id,
            "vote": self.vote,
            "reason": self.reason
        }
