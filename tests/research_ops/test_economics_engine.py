from aidp.research_ops.economics_engine import EconomicsEngine, ScientificTaskProposal


def test_economics_priority_scoring() -> None:
    engine = EconomicsEngine()

    high_impact_cheap_task = ScientificTaskProposal(
        id="t1",
        name="Good",
        expected_impact=0.9,
        information_gain=0.9,
        novelty=0.8,
        estimated_cost_usd=1.0,
        estimated_time_hours=1.0,
        risk_of_failure=0.1,
    )

    low_impact_expensive_task = ScientificTaskProposal(
        id="t2",
        name="Bad",
        expected_impact=0.2,
        information_gain=0.1,
        novelty=0.1,
        estimated_cost_usd=100.0,
        estimated_time_hours=10.0,
        risk_of_failure=0.9,
    )

    score1 = engine.calculate_priority_score(high_impact_cheap_task)
    score2 = engine.calculate_priority_score(low_impact_expensive_task)

    assert score1 > score2
    assert score1 > 0.0
