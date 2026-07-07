from aidp.research_ops.budget_controller import BudgetController, OperatingMode


def test_budget_thresholds() -> None:
    controller = BudgetController(daily_token_budget=1000)

    assert controller.operating_mode == OperatingMode.NORMAL

    # Consume 85%
    controller.log_token_usage(850)
    assert controller.operating_mode == OperatingMode.CONSERVE_TOKENS

    # Consume another 10%
    controller.log_token_usage(100)
    assert controller.operating_mode == OperatingMode.PAUSE_EXPENSIVE

    # Exceed budget
    controller.log_token_usage(100)
    assert controller.operating_mode == OperatingMode.HALT
