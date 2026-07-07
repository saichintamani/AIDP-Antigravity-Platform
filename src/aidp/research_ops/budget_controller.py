from enum import Enum


class OperatingMode(Enum):
    NORMAL = "normal"
    CONSERVE_TOKENS = "conserve_tokens"
    PAUSE_EXPENSIVE = "pause_expensive"
    HALT = "halt"


class BudgetController:
    """
    Governs daily and monthly lab spend, forcing operational mode changes
    when thresholds are breached.
    """

    def __init__(self, daily_token_budget: int = 1_000_000) -> None:
        self.daily_token_budget = daily_token_budget
        self.tokens_consumed = 0
        self.operating_mode = OperatingMode.NORMAL

    def log_token_usage(self, tokens: int) -> None:
        self.tokens_consumed += tokens
        self._evaluate_thresholds()

    def _evaluate_thresholds(self) -> None:
        percent_used = self.tokens_consumed / self.daily_token_budget
        if percent_used >= 1.0:
            self.operating_mode = OperatingMode.HALT
        elif percent_used >= 0.9:
            self.operating_mode = OperatingMode.PAUSE_EXPENSIVE
        elif percent_used >= 0.8:
            self.operating_mode = OperatingMode.CONSERVE_TOKENS
        else:
            self.operating_mode = OperatingMode.NORMAL
