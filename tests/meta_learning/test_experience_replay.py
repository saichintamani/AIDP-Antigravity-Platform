from aidp.meta_learning.discovery_memory import DiscoveryMemory
from aidp.meta_learning.experience_replay import ExperienceReplayEngine


def test_experience_replay() -> None:
    mem = DiscoveryMemory(":memory:")
    mem.log_campaign("Find cancer cure", "oncology", 0.1, 500.0, "failed")

    engine = ExperienceReplayEngine(mem)
    context = engine.generate_context_for_planner("oncology")

    assert "AVOID REPEATING THESE PAST FAILURES" in context
    assert "Find cancer cure" in context
