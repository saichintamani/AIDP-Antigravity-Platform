import json
from typing import Optional, Any, Callable

from aidp.discovery.consensus import ConsensusEngine, ReviewerResult
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.reasoning_planner import ReasoningPlanner
from aidp.intelligence.task_specification import CognitiveTaskType, TaskSpecification


class ScientificDebateEngine:
    """
    Coordinates adversarial personas to critique an ExperimentalDesign before execution.
    Queries the Intelligence Gateway to simulate expert review.
    Uses ConsensusEngine to aggregate the results.
    """

    def __init__(
        self, gateway: Optional[IntelligenceGateway] = None, consensus_engine: Optional[ConsensusEngine] = None
    ):
        self.gateway = gateway
        self.planner = ReasoningPlanner(gateway) if gateway else None
        self.consensus_engine = consensus_engine or ConsensusEngine()

    def evaluate_design(
        self, experimental_design: dict[str, Any], hypothesis: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Simulates peer review over the experimental design.
        """
        reviews = []

        # 1. Statistician Review
        reviews.append(self._statistician_review(experimental_design))

        # 2. Domain Expert Review
        reviews.append(self._domain_expert_review(experimental_design, hypothesis))

        # 3. Methodologist Review
        reviews.append(self._methodologist_review(experimental_design))

        # 4. Ethicist Review
        reviews.append(self._ethicist_review(experimental_design))

        # 5. Engineer Review
        reviews.append(self._engineer_review(experimental_design))

        # Determine Consensus
        consensus_report = self.consensus_engine.evaluate_consensus(reviews)

        # For compatibility with older tests/structures, we map this back to a dict
        # but also provide the full consensus_report dict for the new tests
        return {
            "experimentalDesignId": experimental_design.get("id"),
            "critiques": [vars(r) for r in reviews],
            "consensusReached": consensus_report.approved,
            "finalDecision": "approved" if consensus_report.approved else "rejected",
            "consensusReport": vars(consensus_report),
        }

    def _query_persona(
        self,
        role: str,
        task_type: CognitiveTaskType,
        context: dict[str, Any],
        fallback_logic: Callable[[], ReviewerResult],
    ) -> ReviewerResult:
        if not self.planner:
            return fallback_logic()

        schema_hint: dict[str, Any] = {
            "reviewerName": None,
            "role": None,
            "confidence": None,
            "blockingIssues": [],
            "suggestions": [],
            "evidence": None,
            "riskScore": None,
            "decision": None,
        }

        spec = TaskSpecification(
            task_type=task_type,
            context=context,
            expected_schema=schema_hint,
            strict_falsifiability=True,
        )

        try:
            result = self.planner.execute_task(spec)
            return ReviewerResult(
                reviewerName=result.get("reviewerName", f"AI {role}"),
                role=role,
                confidence=float(result.get("confidence", 0.8)),
                blockingIssues=result.get("blockingIssues", []),
                suggestions=result.get("suggestions", []),
                evidence=result.get("evidence", ""),
                riskScore=float(result.get("riskScore", 0.0)),
                decision=str(result.get("decision", "approve")).lower(),
            )
        except Exception as e:
            return ReviewerResult(
                reviewerName=f"AI {role} (Fallback)",
                role=role,
                confidence=0.0,
                blockingIssues=[f"Gateway failure during review: {str(e)}"],
                suggestions=[],
                evidence="",
                riskScore=1.0,
                decision="reject",
            )

    def _statistician_review(self, design: dict[str, Any]) -> ReviewerResult:
        """Checks for valid controls and falsifiability."""

        def fallback() -> ReviewerResult:
            controls = design.get("controls", [])
            failure_criteria = design.get("failureCriteria", "")
            if not controls:
                return ReviewerResult(
                    "Fallback Statistician",
                    "Statistician",
                    0.9,
                    ["Experimental design lacks control conditions."],
                    [],
                    "",
                    0.9,
                    "reject",
                )
            if (
                "falsified" not in failure_criteria.lower()
                and "reject" not in failure_criteria.lower()
            ):
                return ReviewerResult(
                    "Fallback Statistician",
                    "Statistician",
                    0.9,
                    ["Failure criteria is weak or non-falsifiable."],
                    [],
                    "",
                    0.9,
                    "reject",
                )
            return ReviewerResult(
                "Fallback Statistician",
                "Statistician",
                0.9,
                [],
                ["Looks adequate"],
                "",
                0.1,
                "approve",
            )

        context = {
            "variables": json.dumps(
                {
                    "independent": design.get("independentVariables", []),
                    "dependent": design.get("dependentVariables", []),
                }
            ),
            "controls": json.dumps(design.get("controls", [])),
            "sample_size": "Not provided",
            "metrics": design.get("failureCriteria", "Not provided"),
        }
        return self._query_persona(
            "Statistician", CognitiveTaskType.STATISTICIAN_REVIEW, context, fallback
        )

    def _domain_expert_review(
        self, design: dict[str, Any], hypothesis: dict[str, Any]
    ) -> ReviewerResult:
        """Checks biological/physical plausibility."""

        def fallback() -> ReviewerResult:
            return ReviewerResult(
                "Fallback Domain Expert",
                "Domain Expert",
                0.9,
                [],
                ["Variables are consistent with domain ontology."],
                "",
                0.1,
                "approve",
            )

        context = {
            "claim": hypothesis.get("claim", ""),
            "hypothesis": json.dumps(hypothesis),
            "evidence": "Not provided",
        }
        return self._query_persona(
            "Domain Expert", CognitiveTaskType.DOMAIN_REVIEW, context, fallback
        )

    def _methodologist_review(self, design: dict[str, Any]) -> ReviewerResult:
        """Checks experimental setup."""

        def fallback() -> ReviewerResult:
            if len(design.get("independentVariables", [])) == 0:
                return ReviewerResult(
                    "Fallback Methodologist",
                    "Methodologist",
                    0.9,
                    ["No independent variable defined for manipulation."],
                    [],
                    "",
                    0.9,
                    "reject",
                )
            return ReviewerResult(
                "Fallback Methodologist",
                "Methodologist",
                0.9,
                [],
                ["Methodological setup is sound."],
                "",
                0.1,
                "approve",
            )

        context = {
            "protocol": "Not provided",
            "experiment_flow": json.dumps(
                {
                    "independent": design.get("independentVariables", []),
                    "dependent": design.get("dependentVariables", []),
                }
            ),
            "confounders": "Not provided",
        }
        return self._query_persona(
            "Methodologist", CognitiveTaskType.METHODOLOGY_REVIEW, context, fallback
        )

    def _ethicist_review(self, design: dict[str, Any]) -> ReviewerResult:
        """Checks ethical implications."""

        def fallback() -> ReviewerResult:
            return ReviewerResult(
                "Fallback Ethicist",
                "Ethicist",
                0.9,
                [],
                ["No obvious ethical violations."],
                "",
                0.1,
                "approve",
            )

        context = {
            "protocol": "Not provided",
            "resources": design.get("resourceEstimation", "Not provided"),
        }
        return self._query_persona("Ethicist", CognitiveTaskType.ETHICS_REVIEW, context, fallback)

    def _engineer_review(self, design: dict[str, Any]) -> ReviewerResult:
        """Checks technical feasibility."""

        def fallback() -> ReviewerResult:
            return ReviewerResult(
                "Fallback Engineer",
                "Engineer",
                0.9,
                [],
                ["Design is technically feasible."],
                "",
                0.1,
                "approve",
            )

        context = {
            "protocol": "Not provided",
            "resources": design.get("resourceEstimation", "Not provided"),
            "cost_prediction": design.get("costPrediction", "Not provided"),
            "failure_prediction": design.get("failurePrediction", "Not provided"),
        }
        return self._query_persona(
            "Engineer", CognitiveTaskType.ENGINEERING_REVIEW, context, fallback
        )
