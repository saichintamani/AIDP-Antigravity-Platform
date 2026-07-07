from dataclasses import dataclass


@dataclass
class UncertaintyAttribution:
    model: float
    retrieval: float
    knowledge: float
    tool: float
    planning: float
    observation: float

    @property
    def total_uncertainty(self) -> float:
        """Simple arithmetic mean of all uncertainty vectors for a summary score."""
        return (
            sum(
                [
                    self.model,
                    self.retrieval,
                    self.knowledge,
                    self.tool,
                    self.planning,
                    self.observation,
                ]
            )
            / 6.0
        )


class UncertaintyEngine:
    def __init__(self) -> None:
        pass

    def estimate_uncertainty(
        self, retrieval_scores: list[float], model_confidence: float
    ) -> UncertaintyAttribution:
        """
        Calculates distinct uncertainty vectors for a reasoning step.
        (Lower is better/more certain).
        """
        # MOCK IMPLEMENTATION
        retrieval_unc = (
            1.0 - (sum(retrieval_scores) / len(retrieval_scores)) if retrieval_scores else 1.0
        )

        return UncertaintyAttribution(
            model=1.0 - model_confidence,
            retrieval=retrieval_unc,
            knowledge=0.2,  # Baseline epistemic uncertainty
            tool=0.0,  # Deterministic tools
            planning=0.1,  # Minor planning branching uncertainty
            observation=0.0,  # Clean parsed text
        )
