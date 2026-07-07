from aidp.cognitive_core.curiosity_engine import CuriosityEngine, ResearchDirection


def test_curiosity_score() -> None:
    engine = CuriosityEngine()

    dir1 = ResearchDirection("id1", "desc1", "target1", [])

    # By default, our mock heuristics return positive values.
    score = engine.score_direction(dir1)

    # 0.8 + 0.9 + 0.7 + 0.6 - 0.4 = 2.6
    assert abs(score - 2.6) < 0.01
