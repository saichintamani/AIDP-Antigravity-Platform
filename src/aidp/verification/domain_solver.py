from typing import Any


class DomainSolver:
    """
    Level 3: Domain Constraints
    Hardcodes critical domain failure modes to catch overfitting.
    """

    def verify(self, protocol: dict[str, Any]) -> dict[str, Any]:
        protocol_str = str(protocol).lower()
        
        # Check for Vehicle Control in Human Trials (Phase 5 Failure Mode)
        is_human = "human" in protocol_str or "clinical" in protocol_str
        has_vehicle = "vehicle" in protocol_str
        
        if is_human and has_vehicle:
            return {
                "status": "FAILED",
                "reason": "INVALID: Vehicle controls are not allowed for human clinical trials."
            }
            
        return {
            "status": "PASS",
            "reason": "Domain constraints validated."
        }
