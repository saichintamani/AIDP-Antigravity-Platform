from aidp.reasoning.multi_agent_consensus import MultiAgentConsensus
from aidp.reasoning.subjective_logic import Opinion


def test_multi_agent_consensus() -> None:
    # Op1: High belief (Statistician)
    op1 = Opinion(belief=0.8, disbelief=0.1, uncertainty=0.1, base_rate=0.5)

    # Op2: High disbelief (Reviewer)
    op2 = Opinion(belief=0.1, disbelief=0.8, uncertainty=0.1, base_rate=0.5)

    # Fuse them
    fused = MultiAgentConsensus.fuse_laboratory_opinions([op1, op2])

    # Conflicting high certainty opinions should result in balanced belief and disbelief
    assert abs(fused.belief - fused.disbelief) < 0.01
    assert fused.uncertainty < 0.1
