from aidp.cognitive_core.strategy_planner import StrategyPlanner


def test_strategy_planner_ranking() -> None:
    planner = StrategyPlanner()

    hypotheses = [
        {"id": "h1", "impact": 0.9, "cost": 0.1},  # Score: 9.0 (Best)
        {"id": "h2", "impact": 0.5, "cost": 0.5},  # Score: 1.0
        {"id": "h3", "impact": 0.1, "cost": 0.9},  # Score: 0.11 (Worst)
        {"id": "h4", "impact": 0.8, "cost": 0.2},  # Score: 4.0 (Second Best)
    ]

    selected = planner.rank_and_select(hypotheses, top_n=2)

    assert len(selected) == 2
    assert selected[0]["id"] == "h1"
    assert selected[1]["id"] == "h4"
