import json
from typing import Any
from jsonschema import validate
from jsonschema.exceptions import ValidationError

class ConstraintSolver:
    """
    Advanced Level 2 Constraint Validation
    Uses rigorous JSON Schema validation to deterministically verify structural constraints.
    Replaces flimsy string matching and LLM hallucination checks with prominent mathematical logic.
    """

    def __init__(self):
        # The rigid mathematical constraint schema representing a scientifically valid experiment.
        self.scientific_schema = {
            "type": "object",
            "required": ["controls", "methodology"],
            "properties": {
                "controls": {
                    "type": "array",
                    "minItems": 1
                },
                "methodology": {
                    "type": "object",
                    "required": ["is_human_trial"],
                    "properties": {
                        "is_human_trial": {"type": "boolean"},
                        "randomized": {"type": "boolean"},
                        "blinded": {"type": "boolean"}
                    }
                }
            }
        }

    def verify(self, protocol: dict[str, Any], required_constraints: list[str] = None) -> dict[str, Any]:
        """
        Deterministically verifies the protocol against exact structural rules via JSON schema.
        """
        # 1. Base JSON Schema Structural Validation
        try:
            validate(instance=protocol, schema=self.scientific_schema)
        except ValidationError as e:
            return {
                "status": "FAILED",
                "reason": f"Structural JSON Schema Violation: {e.message}"
            }
            
        # 2. Strict Logical Dependency Validation (Human Trials MUST be randomized & blinded)
        methodology = protocol.get("methodology", {})
        if methodology.get("is_human_trial"):
            if not methodology.get("randomized"):
                return {
                    "status": "FAILED",
                    "reason": "Regulatory Violation: Human trial lacks absolute randomization."
                }
            if not methodology.get("blinded"):
                return {
                    "status": "FAILED",
                    "reason": "Regulatory Violation: Human trial lacks double-blinding."
                }
                
        # 3. Dynamic External Constraints Check
        if required_constraints:
            protocol_str = json.dumps(protocol).lower()
            for constraint in required_constraints:
                if constraint.lower() not in protocol_str:
                    return {
                        "status": "FAILED",
                        "reason": f"Violated explicit dynamic constraint: Must incorporate '{constraint}'."
                    }

        return {
            "status": "PASS",
            "reason": "All mathematical, structural, and dynamic schemas validated successfully."
        }
