"""
Multi-Dimensional Rubric Judge for Scientific Hypothesis Evaluation
===================================================================
Inspired by:
  - HypoBench: Decomposed scoring across Grounding, Novelty, Testability, Explanatory Power
  - Sakana AI Scientist: ICLR-calibrated automated reviewer with ensemble scoring
  - ProjectionBench: Progressive information disclosure evaluation

Scores hypotheses across 5 independent axes rather than a single boolean.
"""
import json
from typing import Any

from pydantic import BaseModel, Field


class JudgeVerdict(BaseModel):
    """Structured multi-dimensional evaluation of a generated hypothesis."""
    
    # Per-dimension scores (0.0 = worst, 1.0 = best)
    scientific_grounding: float = Field(
        ..., ge=0.0, le=1.0,
        description="Does the hypothesis align with and correctly reference the provided evidence?"
    )
    mechanistic_accuracy: float = Field(
        ..., ge=0.0, le=1.0,
        description="Does it capture the correct causal mechanism of the historical breakthrough?"
    )
    testability: float = Field(
        ..., ge=0.0, le=1.0,
        description="Is the experimental design concrete, falsifiable, and executable?"
    )
    novelty: float = Field(
        ..., ge=0.0, le=1.0,
        description="Does it go beyond restating the evidence to propose a genuinely new insight?"
    )
    constraint_compliance: float = Field(
        ..., ge=0.0, le=1.0,
        description="Does it satisfy all mathematical/physical constraints without violation?"
    )
    
    # Aggregate and metadata
    overall_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Weighted average across all dimensions"
    )
    is_match: bool = Field(
        ..., description="True if the hypothesis fundamentally captures the historical breakthrough"
    )
    reasoning: str = Field(
        ..., description="Step-by-step reasoning from the judge"
    )
    failure_mode: str | None = Field(
        default=None,
        description="If is_match is False, the primary failure category"
    )


# Weights for the overall score calculation
DIMENSION_WEIGHTS = {
    "scientific_grounding": 0.25,
    "mechanistic_accuracy": 0.30,
    "testability": 0.15,
    "novelty": 0.10,
    "constraint_compliance": 0.20,
}


class RubricJudge:
    """
    Multi-dimensional hypothesis evaluator.
    
    Can operate in two modes:
      - LLM mode: Uses a real LLM via the IntelligenceGateway
      - Mock mode: Returns deterministic scores for architectural testing
    """
    
    def __init__(self, gateway=None):
        self.gateway = gateway
    
    def evaluate(
        self,
        hypothesis_text: str,
        historical_winner: str,
        constraints: list[str] | None = None,
        evidence_summary: str = "",
    ) -> JudgeVerdict:
        """
        Evaluate a hypothesis against the historical ground truth
        using a multi-dimensional rubric.
        """
        if self.gateway is None:
            return self._mock_evaluate(hypothesis_text, historical_winner)
        
        return self._llm_evaluate(
            hypothesis_text, historical_winner, constraints or [], evidence_summary
        )
    
    def _llm_evaluate(
        self,
        hypothesis_text: str,
        historical_winner: str,
        constraints: list[str],
        evidence_summary: str,
    ) -> JudgeVerdict:
        """Uses an LLM to score the hypothesis across 5 dimensions."""
        constraints_text = "\n".join(f"- {c}" for c in constraints) if constraints else "None specified."
        
        prompt = f"""You are a rigorous scientific evaluation judge.
Score the GENERATED HYPOTHESIS against the HISTORICAL BREAKTHROUGH across 5 dimensions.

HISTORICAL BREAKTHROUGH (Ground Truth):
{historical_winner}

GENERATED HYPOTHESIS:
{hypothesis_text}

EVIDENCE CONTEXT:
{evidence_summary[:500] if evidence_summary else "Not provided."}

CONSTRAINTS:
{constraints_text}

Score each dimension from 0.0 to 1.0:
1. scientific_grounding: Does it correctly reference the evidence?
2. mechanistic_accuracy: Does it capture the same causal mechanism as the breakthrough?
3. testability: Is the experimental design concrete and falsifiable?
4. novelty: Does it propose something beyond restating evidence?
5. constraint_compliance: Does it satisfy all constraints?

Also determine:
- is_match: true if the hypothesis fundamentally captures the core insight
- failure_mode: If is_match is false, one of: CONSTRAINT_VIOLATION, TEMPORAL_LEAK, MECHANISM_MISS, HALLUCINATION, ADVERSARY_REJECTION, null if match

Respond ONLY with this JSON:
{{"scientific_grounding": 0.0, "mechanistic_accuracy": 0.0, "testability": 0.0, "novelty": 0.0, "constraint_compliance": 0.0, "is_match": false, "reasoning": "your reasoning", "failure_mode": null}}"""

        try:
            schema_hint = {
                "scientific_grounding": 0.5,
                "mechanistic_accuracy": 0.5,
                "testability": 0.5,
                "novelty": 0.5,
                "constraint_compliance": 0.5,
                "is_match": False,
                "reasoning": "string",
                "failure_mode": None,
            }
            data = self.gateway.query(prompt, schema_hint=schema_hint)
            
            # Compute weighted overall score
            overall = sum(
                float(data.get(dim, 0.0)) * weight
                for dim, weight in DIMENSION_WEIGHTS.items()
            )
            
            return JudgeVerdict(
                scientific_grounding=float(data.get("scientific_grounding", 0.0)),
                mechanistic_accuracy=float(data.get("mechanistic_accuracy", 0.0)),
                testability=float(data.get("testability", 0.0)),
                novelty=float(data.get("novelty", 0.0)),
                constraint_compliance=float(data.get("constraint_compliance", 0.0)),
                overall_score=round(overall, 3),
                is_match=bool(data.get("is_match", False)),
                reasoning=str(data.get("reasoning", "")),
                failure_mode=data.get("failure_mode"),
            )
        except Exception as e:
            # On LLM failure, return a conservative verdict
            return JudgeVerdict(
                scientific_grounding=0.0,
                mechanistic_accuracy=0.0,
                testability=0.0,
                novelty=0.0,
                constraint_compliance=0.0,
                overall_score=0.0,
                is_match=False,
                reasoning=f"Judge evaluation failed: {e}",
                failure_mode="JSON_PARSE_FAILURE",
            )
    
    def _mock_evaluate(
        self, hypothesis_text: str, historical_winner: str
    ) -> JudgeVerdict:
        """Deterministic mock evaluation for architectural testing."""
        # Simple heuristic: if hypothesis has content, give moderate scores
        has_content = len(hypothesis_text) > 20
        
        return JudgeVerdict(
            scientific_grounding=0.75 if has_content else 0.0,
            mechanistic_accuracy=0.70 if has_content else 0.0,
            testability=0.80 if has_content else 0.0,
            novelty=0.60 if has_content else 0.0,
            constraint_compliance=0.85 if has_content else 0.0,
            overall_score=0.74 if has_content else 0.0,
            is_match=has_content,
            reasoning="Mock evaluation: hypothesis has sufficient content" if has_content else "Mock evaluation: empty hypothesis",
            failure_mode=None if has_content else "MECHANISM_MISS",
        )
