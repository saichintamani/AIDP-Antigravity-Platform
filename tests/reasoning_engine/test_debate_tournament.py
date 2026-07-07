from aidp.reasoning.subjective_logic import Opinion
from aidp.reasoning_engine.reviewer_tournament import ReviewerTournament


def test_reviewer_tournament_filters_hallucination() -> None:
    tournament = ReviewerTournament()

    # 3 reviewers agree, 1 hallucinates
    o1 = Opinion(belief=0.8, disbelief=0.1, uncertainty=0.1, base_rate=0.5)
    o2 = Opinion(belief=0.75, disbelief=0.15, uncertainty=0.1, base_rate=0.5)
    o3 = Opinion(belief=0.85, disbelief=0.05, uncertainty=0.1, base_rate=0.5)
    hallucination = Opinion(belief=0.0, disbelief=0.9, uncertainty=0.1, base_rate=0.5)

    fused = tournament.run_tournament("Hypothesis X", [o1, o2, o3, hallucination])

    # Fusion should heavily weight the consensus (belief > disbelief)
    assert fused.belief > fused.disbelief
