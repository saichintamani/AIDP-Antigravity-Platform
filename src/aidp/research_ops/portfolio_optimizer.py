

class PortfolioOptimizer:
    """
    Distributes resources dynamically across scientific domains based on expected value.
    """

    def __init__(self) -> None:
        # Target allocations (percentages)
        self.target_allocation: dict[str, float] = {
            "Cancer": 0.35,
            "Drug Discovery": 0.25,
            "Genomics": 0.20,
            "Virology": 0.20,
        }

    def get_domain_budget_multiplier(
        self, domain: str, current_spend_distribution: dict[str, float]
    ) -> float:
        """
        Returns a multiplier to adjust task priority based on portfolio balance.
        If a domain is under-funded relative to target, it gets a >1.0 multiplier.
        """
        target = self.target_allocation.get(domain, 0.0)
        if target == 0.0:
            return 0.1  # Heavy penalty for off-portfolio work

        current = current_spend_distribution.get(domain, 0.0)

        # If we've spent 0, give it a big boost to catch up
        if current == 0.0:
            return 2.0

        # e.g. Target 0.35, Current 0.17 -> 0.35 / 0.17 = 2.05 multiplier
        multiplier = target / current

        # Cap multiplier to prevent runaway priority
        return min(max(multiplier, 0.1), 3.0)
