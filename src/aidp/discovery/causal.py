from typing import Optional, Any


class CausalDiscoveryEngine:
    """
    Evaluates hypotheses using Structural Causal Models (SCMs) and Do-calculus heuristics.
    Separates simple observational correlation from true causal intervention.
    """

    def __init__(self) -> None:
        pass

    def detect_backdoor_paths(
        self, causal_graph: dict[str, Any], source: str, target: str
    ) -> list[str]:
        """
        Identifies unobserved confounders or backdoor paths that could explain the correlation
        between source and target without a direct causal link.
        """
        backdoors = []

        # MOCK IMPLEMENTATION
        # In M9+, this uses proper DAG traversal to check for d-separation.

        confounders = causal_graph.get("unobservedConfounders", [])
        for confounder in confounders:
            # Simple string parsing of mock format "U->A,B"
            if "->" in confounder:
                parts = confounder.split("->")
                u_node = parts[0]
                targets = parts[1].split(",")
                if source in targets and target in targets:
                    backdoors.append(u_node)

        return backdoors

    def simulate_intervention(
        self,
        hypothesis: dict[str, Any],
        causal_graph: dict[str, Any],
        ledger_entry: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Calculates the theoretical effect of do(X=x) on the hypothesis.
        If a backdoor path dominates, the intervention effect collapses.
        Enforces M9.25 Scientific Governance gate.
        """
        if not ledger_entry:
            raise ValueError(
                "Hypothesis lacks provenance. A ledger_entry is required to enter causal analysis."
            )

        readiness = ledger_entry.get("readiness")
        if readiness not in ["readyForCausal", "readyForExperiment"]:
            raise ValueError(
                f"Hypothesis failed M9.25 governance gate. Readiness level '{readiness}' is insufficient for causal analysis."
            )

        updated_hypothesis = dict(hypothesis)

        # Parse claim "A causally induces B" to extract nodes
        # This is a mock extraction for structural validation
        claim = hypothesis.get("claim", "")
        source = "A"
        target = "B"
        if " causally induces " in claim:
            parts = claim.split(" causally induces ")
            source = parts[0]
            target = parts[1].strip(".")

        backdoors = self.detect_backdoor_paths(causal_graph, source, target)

        if backdoors:
            # The correlation is heavily confounded. The causal hypothesis degrades.
            updated_hypothesis["confidence"] = max(
                0.0, updated_hypothesis.get("confidence", 0.5) - 0.4
            )
            updated_hypothesis["risk"] = min(1.0, updated_hypothesis.get("risk", 0.0) + 0.5)
            updated_hypothesis["causal_validation_failed"] = True
            updated_hypothesis["confounders_detected"] = backdoors
        else:
            # No backdoors detected, causal claim strengthens structurally
            updated_hypothesis["confidence"] = min(
                1.0, updated_hypothesis.get("confidence", 0.5) + 0.2
            )

        return updated_hypothesis
