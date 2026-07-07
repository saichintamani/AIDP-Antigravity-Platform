
from aidp.reasoning.subjective_logic import Opinion, consensus_fusion


class MultiAgentConsensus:
    """
    Fuses opinions from multiple specialized agents (e.g., Methodologist, Statistician, Reviewer).
    """

    @staticmethod
    def fuse_laboratory_opinions(opinions: list[Opinion]) -> Opinion:
        """
        Takes a list of Opinions from various agents and mathematically fuses them
        using Subjective Logic's consensus operator.
        """
        if not opinions:
            return Opinion(0.0, 0.0, 1.0, 0.5)

        if len(opinions) == 1:
            return opinions[0]

        # Successively fuse the opinions
        fused_opinion = opinions[0]
        for op in opinions[1:]:
            fused_opinion = consensus_fusion(fused_opinion, op)

        return fused_opinion
