from typing import Any

from aidp.verification.assumption_solver import AssumptionSolver
from aidp.verification.constraint_solver import ConstraintSolver
from aidp.verification.domain_solver import DomainSolver
from aidp.verification.statistical_solver import StatisticalSolver


class FormalVerificationEngine:
    """
    Orchestrates the 4-Level Verification Pipeline.
    If any level fails, the entire protocol is flagged as FAILED.
    """
    
    def __init__(self, world_model=None):
        self.level_1 = StatisticalSolver()
        self.level_2 = ConstraintSolver()
        self.level_3 = DomainSolver()
        self.level_4 = AssumptionSolver(world_model)
        
    def run(self, protocol: dict[str, Any]) -> dict[str, Any]:
        """
        Executes all 4 levels of formal verification on the provided protocol.
        Generates Ontology-Aware confidence scores.
        """
        report = {
            "status": "PASS",
            "levels": {},
            "ontology": {
                "verification_confidence": 1.0,
                "assumption_confidence": 1.0,
                "evidence_confidence": 1.0,
                "reproducibility_confidence": 1.0
            }
        }
        
        # Level 1: Statistical Verification
        l1_result = self.level_1.verify(protocol)
        report["levels"]["level_1_statistical"] = l1_result
        if l1_result.get("status") == "FAILED":
            report["status"] = "FAILED"
            report["blocking_reason"] = l1_result.get("reason")
            report["ontology"]["verification_confidence"] *= 0.0
            return report
            
        # Level 2: Constraint Validation
        l2_result = self.level_2.verify(protocol)
        report["levels"]["level_2_constraint"] = l2_result
        if l2_result.get("status") == "FAILED":
            report["status"] = "FAILED"
            report["blocking_reason"] = l2_result.get("reason")
            report["ontology"]["verification_confidence"] *= 0.0
            return report
            
        # Level 3: Domain Constraints
        l3_result = self.level_3.verify(protocol)
        report["levels"]["level_3_domain"] = l3_result
        if l3_result.get("status") == "FAILED":
            report["status"] = "FAILED"
            report["blocking_reason"] = l3_result.get("reason")
            report["ontology"]["evidence_confidence"] *= 0.0
            report["ontology"]["reproducibility_confidence"] *= 0.0
            return report
            
        # Level 4: Assumption Verification
        l4_result = self.level_4.verify(protocol)
        report["levels"]["level_4_assumption"] = l4_result
        
        # Assumption penalty scales with how many failed.
        failed_assumptions = l4_result.get("failed_assumptions", [])
        total_assumptions = len(protocol.get("assumptions", []))
        if total_assumptions > 0:
            penalty = len(failed_assumptions) / total_assumptions
            report["ontology"]["assumption_confidence"] = max(0.0, 1.0 - penalty)
            
            # If all assumptions fail, it's a fatal rejection
            if penalty == 1.0:
                report["status"] = "FAILED"
                report["blocking_reason"] = "All critical assumptions failed verification against the World Model."
                return report
                
        # Phase 15: Level 5 - Constraint Intelligence (Symbolic SAT Checking)
        from aidp.intelligence.epistemic_models import Claim
        from aidp.intelligence.symbolic_solver import ConstraintIntelligenceEngine
        
        engine_ci = ConstraintIntelligenceEngine()
        claims = []
        
        # 1. Protocol Logic
        has_control = protocol.get("design", {}).get("has_control_group", True)
        power = protocol.get("statistical_power", 0.85)
        claims.append(Claim(
            claim_text="Protocol Logic",
            assumptions=[],
            symbolic_formulation={"type": "protocol_logic", "has_control": has_control, "power": power},
            generated_by="FormalVerificationEngine"
        ))
            
        # 2. Resource Exhaustion
        patients = protocol.get("patients", 100)
        clinics = protocol.get("total_clinics", 5)
        ppc = protocol.get("patients_per_clinic", 20)
        claims.append(Claim(
            claim_text="Resource Constraints",
            assumptions=[],
            symbolic_formulation={"type": "resource_capacity", "required_patients": patients, "total_clinics": clinics, "patients_per_clinic": ppc},
            generated_by="FormalVerificationEngine"
        ))
            
        # 3. Temporal Causality (If schedule exists)
        if "schedule" in protocol:
            events = protocol["schedule"].get("events", {})
            constraints = protocol["schedule"].get("constraints", [])
            for evt, t in events.items():
                claims.append(Claim(
                    claim_text=f"Event {evt}",
                    assumptions=[],
                    symbolic_formulation={"type": "temporal_event", "event": evt, "time": t},
                    generated_by="FormalVerificationEngine"
                ))
            for prior, subseq in constraints:
                claims.append(Claim(
                    claim_text=f"Order {prior} -> {subseq}",
                    assumptions=[],
                    symbolic_formulation={"type": "temporal_order", "prior": prior, "subsequent": subseq},
                    generated_by="FormalVerificationEngine"
                ))

        proof = engine_ci.evaluate_claims(claims)
        if not proof.is_valid:
            report["status"] = "FAILED"
            report["blocking_reason"] = f"Symbolic Proof FAILED: {proof.message}"
            return report

        report["levels"]["level_5_symbolic"] = {"status": "PASSED", "reason": "All mathematical constraints proved SAT."}
        
        return report
