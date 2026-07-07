from aidp.meta_learning.prompt_evolution import PromptRegistry


def test_prompt_evolution() -> None:
    registry = PromptRegistry()
    registry.register_prompt("statistician", "v1", "You are a statistician.")
    registry.register_prompt("statistician", "v2", "You are a strict statistician. Check power.")

    # Use v1 and it gets low score
    registry.log_performance("statistician", "You are a statistician.", 0.2)

    # Use v2 and it gets high score
    registry.log_performance("statistician", "You are a strict statistician. Check power.", 0.9)

    best = registry.get_best_prompt("statistician")
    assert best == "You are a strict statistician. Check power."
