
from aidp.intelligence.agents.personas import ReviewerAgent
from aidp.reasoning.subjective_logic import Opinion, consensus_fusion


class ReviewerTournament:
    """
    Pools independent reviewers to evaluate a claim and mathematically fuses
    their opinions to filter out hallucinations.
    """

    def __init__(self) -> None:
        self.reviewers: list[ReviewerAgent] = []

    def run_tournament(self, claim: str, reviewer_opinions: list[Opinion]) -> Opinion:
        if not reviewer_opinions:
            raise ValueError("No reviewers provided")

        fused = reviewer_opinions[0]
        for op in reviewer_opinions[1:]:
            fused = consensus_fusion(fused, op)

        return fused
