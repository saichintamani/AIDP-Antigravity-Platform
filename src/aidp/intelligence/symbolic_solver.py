
import z3
from pydantic import BaseModel

from aidp.intelligence.epistemic_models import Claim


class ContradictionProof(BaseModel):
    is_valid: bool
    message: str
    conflicting_claim_ids: list[str] = []
    unsat_core: list[str] = []

class ConstraintIntelligenceEngine:
    """
    Central Z3 formulation engine that translates Claims into mathematical constraints
    and extracts Contradiction Proofs via unsat_cores.
    """
    
    def _extract_contradiction_proof(self, solver: z3.Solver, claim_mapping: dict[z3.BoolRef, str]) -> ContradictionProof:
        core = solver.unsat_core()
        conflicting_claims = []
        core_names = []
        for c in core:
            core_names.append(str(c))
            if c in claim_mapping:
                conflicting_claims.append(claim_mapping[c])
                
        return ContradictionProof(
            is_valid=False,
            message="UNSAT: Contradiction detected in the provided claims.",
            conflicting_claim_ids=conflicting_claims,
            unsat_core=core_names
        )

    def evaluate_claims(self, claims: list[Claim]) -> ContradictionProof:
        """
        Evaluates a set of Claims containing symbolic formulations.
        Returns a ContradictionProof if UNSAT.
        """
        solver = z3.Solver()
        
        # We use boolean variables to track which claim asserted which constraint
        claim_trackers: dict[z3.BoolRef, str] = {}
        
        z3_int_vars: dict[str, z3.ArithRef] = {}
        z3_bool_vars: dict[str, z3.BoolRef] = {}
        z3_real_vars: dict[str, z3.ArithRef] = {}
        
        def get_int(name: str):
            if name not in z3_int_vars:
                z3_int_vars[name] = z3.Int(name)
            return z3_int_vars[name]
            
        def get_bool(name: str):
            if name not in z3_bool_vars:
                z3_bool_vars[name] = z3.Bool(name)
            return z3_bool_vars[name]
            
        def get_real(name: str):
            if name not in z3_real_vars:
                z3_real_vars[name] = z3.Real(name)
            return z3_real_vars[name]

        for claim in claims:
            if not claim.symbolic_formulation:
                continue
                
            form = claim.symbolic_formulation
            ctype = form.get("type")
            
            # Create a tracking variable for this claim
            tracker = z3.Bool(f"tracker_{claim.claim_id}")
            claim_trackers[tracker] = claim.claim_id
            
            if ctype == "temporal_event":
                event = form.get("event")
                time = form.get("time")
                var = get_int(event)
                solver.add(var >= 0)
                solver.assert_and_track(var == time, tracker)
                
            elif ctype == "temporal_order":
                prior = form.get("prior")
                subseq = form.get("subsequent")
                p_var = get_int(prior)
                s_var = get_int(subseq)
                solver.assert_and_track(p_var < s_var, tracker)
                
            elif ctype == "resource_capacity":
                req = get_int('required_patients')
                clinics = get_int('total_clinics')
                ppc = get_int('patients_per_clinic')
                
                solver.assert_and_track(req == form.get("required_patients", 0), z3.Bool(f"t_req_{claim.claim_id}"))
                solver.assert_and_track(clinics == form.get("total_clinics", 0), z3.Bool(f"t_clinics_{claim.claim_id}"))
                solver.assert_and_track(ppc == form.get("patients_per_clinic", 0), z3.Bool(f"t_ppc_{claim.claim_id}"))
                
                # claim tracker asserts the relationship
                solver.assert_and_track(req <= clinics * ppc, tracker)
                
            elif ctype == "physical_constraint":
                mass = get_real('mass_X')
                pore = get_real('pore_size_Y')
                
                if "mass_X" in form:
                    solver.assert_and_track(mass == form["mass_X"], z3.Bool(f"t_mass_{claim.claim_id}"))
                if "pore_size_Y" in form:
                    solver.assert_and_track(pore == form["pore_size_Y"], z3.Bool(f"t_pore_{claim.claim_id}"))
                
                rule = form.get("rule")
                if rule == "mass_less_than_pore":
                    solver.assert_and_track(mass < pore, tracker)
                elif rule == "mass_greater_than_pore":
                    solver.assert_and_track(mass > pore, tracker)
                
            elif ctype == "protocol_logic":
                control = get_bool('has_control')
                pwr = get_real('power')
                
                solver.assert_and_track(control == form.get("has_control", False), z3.Bool(f"t_ctrl_{claim.claim_id}"))
                solver.assert_and_track(pwr == form.get("power", 0.0), z3.Bool(f"t_pwr_{claim.claim_id}"))
                
                # Rule: Protocol must have control and high power.
                solver.assert_and_track(control, z3.Bool(f"rule_ctrl_{claim.claim_id}"))
                solver.assert_and_track(pwr >= 0.8, z3.Bool(f"rule_pwr_{claim.claim_id}"))
                
                # (For simplicity, we map rule failures directly to the claim)
                claim_trackers[z3.Bool(f"t_ctrl_{claim.claim_id}")] = claim.claim_id
                claim_trackers[z3.Bool(f"t_pwr_{claim.claim_id}")] = claim.claim_id
                claim_trackers[z3.Bool(f"rule_ctrl_{claim.claim_id}")] = claim.claim_id
                claim_trackers[z3.Bool(f"rule_pwr_{claim.claim_id}")] = claim.claim_id

        if solver.check() == z3.sat:
            return ContradictionProof(is_valid=True, message="SAT: Constraints are mathematically satisfied.")
        else:
            return self._extract_contradiction_proof(solver, claim_trackers)

# For backward compatibility during migration, we can provide wrappers or keep the old classes,
# but the implementation plan specifies refactoring them to use Claims. 
# We'll use ConstraintIntelligenceEngine as the primary entry point now.
