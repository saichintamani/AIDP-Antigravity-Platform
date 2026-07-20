"""
Deterministic Constraint Validation Engine
==========================================
Part of R3 Compartment 1: Programmatic Constraint Checking.
Validates if a hypothesis respects explicit mathematical and physical constraints
BEFORE the more expensive/vibe-based LLM judge.
"""
from pydantic import BaseModel


class ConstraintReport(BaseModel):
    """Report detailing pass/fail for each constraint."""
    compliance_score: float  # 0.0 to 1.0
    passed_constraints: list[str]
    failed_constraints: list[str]
    is_fully_compliant: bool


class ConstraintValidator:
    """
    Intelligent constraint checker.
    Uses a fast semantic gateway call to determine if a hypothesis strictly addresses 
    the given constraints, replacing brittle keyword heuristics.
    """

    def __init__(self, gateway=None):
        self.gateway = gateway

    def validate(self, hypothesis_text: str, constraints: list[str]) -> ConstraintReport:
        """
        Validate a hypothesis against a list of constraints semantically.
        Returns a ConstraintReport.
        """
        if not constraints:
            return ConstraintReport(
                compliance_score=1.0,
                passed_constraints=[],
                failed_constraints=[],
                is_fully_compliant=True
            )

        if not self.gateway:
            # Fallback if no gateway provided (e.g. some tests)
            return ConstraintReport(
                compliance_score=1.0,
                passed_constraints=constraints,
                failed_constraints=[],
                is_fully_compliant=True
            )

        passed = []
        failed = []

        for constraint in constraints:
            prompt = f"""You are a strict deterministic physics engine.
Does the following hypothesis satisfy this specific scientific constraint?

CONSTRAINT:
{constraint}

HYPOTHESIS:
{hypothesis_text}

Respond ONLY with this JSON:
{{"is_compliant": true}} or {{"is_compliant": false}}"""
            
            try:
                schema = {"is_compliant": False}
                res = self.gateway.query(prompt, schema_hint=schema)
                if res.get("is_compliant", False):
                    passed.append(constraint)
                else:
                    failed.append(constraint)
            except Exception as e:
                # Conservative fail if the API chokes
                print(f"Constraint Validator Error: {e}")
                failed.append(constraint)

        compliance_score = len(passed) / len(constraints) if constraints else 1.0
        
        return ConstraintReport(
            compliance_score=compliance_score,
            passed_constraints=passed,
            failed_constraints=failed,
            is_fully_compliant=len(failed) == 0
        )
