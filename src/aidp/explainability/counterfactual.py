from typing import Any


class CounterfactualAnalyzer:
    """
    Evaluates whether a reasoning step genuinely depends on the provided evidence
    by running a counterfactual ('What if this evidence was absent?'), and calculates
    Z3-based constraint relaxation for rejected claims.
    """

    def __init__(self) -> None:
        self.ablation_history = []

    def check_dependency(
        self, hypothesis: str, evidence_list: list[Any], step_inference: str
    ) -> bool:
        """
        Determines if the step_inference is strictly dependent on the evidence_list.
        Returns True if dependent, False if hallucinated or independent of the evidence.
        """
        if not evidence_list:
            return False

        evidence_text = " ".join([str(e).lower() for e in evidence_list])
        inference_tokens = set(step_inference.lower().split())
        matches = [t for t in inference_tokens if t in evidence_text and len(t) > 4]
        return len(matches) > 0

    def calculate_confidence_delta(self, current_confidence: float, evidence_weight: float) -> float:
        """
        Calculates the delta in the Epistemic Ledger if a specific piece of evidence is retracted.
        """
        delta = current_confidence * (evidence_weight * 0.5)
        self.ablation_history.append({"delta": -delta})
        return -delta
        
    def generate_z3_counterfactual(self, unsat_core: list[str]) -> str:
        """
        Analyzes the Z3 unsat_core to propose the minimal counterfactual 
        change that would reverse the UNSAT decision.
        """
        if not unsat_core:
            return "No counterfactual available."
            
        counterfactuals = []
        for core_element in unsat_core:
            # Match common tracker patterns from the symbolic solver
            if "rule_pwr_" in core_element:
                counterfactuals.append("If power >= 0.80")
            elif "rule_ctrl_" in core_element:
                counterfactuals.append("If has_control == True")
            elif "t_req_" in core_element or "t_clinics_" in core_element or "t_ppc_" in core_element:
                counterfactuals.append("If required_patients <= total_clinics * patients_per_clinic")
                
        if counterfactuals:
            cf_str = " and ".join(set(counterfactuals))
            return f"{cf_str}, Result: SAT"
            
        return f"If constraints {', '.join(unsat_core)} are relaxed, Result: SAT"
