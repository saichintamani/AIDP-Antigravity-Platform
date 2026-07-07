from aidp.intelligence.cognition.journal import ReputationSystem


def test_reputation_system() -> None:
    system = ReputationSystem()

    # New agent, default 1.0
    assert system.get_reputation_weight("NewAgent") == 1.0

    # Good agent
    system.log_outcome("GoodAgent", True)
    system.log_outcome("GoodAgent", True)
    assert system.get_reputation_weight("GoodAgent") == 1.0

    # Bad agent
    system.log_outcome("BadAgent", False)
    system.log_outcome("BadAgent", False)
    system.log_outcome("BadAgent", False)
    assert system.get_reputation_weight("BadAgent") < 0.5
