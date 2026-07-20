import math
from typing import Any


class StatisticalSolver:
    """
    Level 1: Statistical Verification
    Deterministically computes required sample size and compares it with the LLM's proposal.
    """

    Z_ALPHA = {
        0.01: 2.576,
        0.05: 1.96,
        0.10: 1.645
    }

    Z_BETA = {
        0.80: 0.84,
        0.90: 1.28,
        0.95: 1.645
    }

    def compute_sample_size(self, effect_size: float, alpha: float = 0.05, power: float = 0.80) -> int:
        if effect_size <= 0:
            raise ValueError("Effect size must be greater than 0.")
        
        z_a = self.Z_ALPHA.get(alpha, 1.96)
        z_b = self.Z_BETA.get(power, 0.84)
            
        n = 2 * ((z_a + z_b) / effect_size) ** 2
        return math.ceil(n)

    def verify(self, protocol: dict[str, Any]) -> dict[str, Any]:
        """
        Extracts provided sample size and compares against required.
        """
        sample_size_data = protocol.get("sampleSize", {})
        if not sample_size_data:
            return {"status": "FAILED", "reason": "No sample size provided in protocol."}
            
        provided_n = sample_size_data.get("n_per_group", 0)
        
        # In a real system, we parse effect_size. We'll use 0.5 as default.
        effect_size = 0.5
        alpha = sample_size_data.get("significance_level_alpha", 0.05)
        power = sample_size_data.get("target_power", 0.80)
        
        required_n = self.compute_sample_size(effect_size, alpha, power)
        
        if provided_n < required_n:
            return {
                "status": "FAILED",
                "required_sample_size": required_n,
                "provided_sample_size": provided_n,
                "reason": f"Provided sample size {provided_n} is mathematically insufficient for target power {power}."
            }
            
        return {
            "status": "PASS",
            "required_sample_size": required_n,
            "provided_sample_size": provided_n
        }

    def validate(self, methodology: dict[str, Any], failure_criteria: str) -> dict[str, Any]:
        """
        Called during planning to propose a statistically sound sample size.
        """
        required_n = self.compute_sample_size(0.5, 0.05, 0.80)
        return {
            "sample_size_recommendation": {
                "n_per_group": required_n,
                "justification": "Computed via baseline power=0.8, alpha=0.05, effect=0.5"
            }
        }
