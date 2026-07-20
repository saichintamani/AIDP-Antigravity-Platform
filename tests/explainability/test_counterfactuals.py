from aidp.explainability.counterfactual import CounterfactualAnalyzer


def test_z3_counterfactual_power():
    analyzer = CounterfactualAnalyzer()
    unsat_core = ["rule_pwr_claim-1", "t_pwr_claim-1"]
    cf = analyzer.generate_z3_counterfactual(unsat_core)
    assert "If power >= 0.80" in cf
    assert "SAT" in cf

def test_z3_counterfactual_control():
    analyzer = CounterfactualAnalyzer()
    unsat_core = ["rule_ctrl_claim-2"]
    cf = analyzer.generate_z3_counterfactual(unsat_core)
    assert "If has_control == True" in cf
    assert "SAT" in cf

def test_z3_counterfactual_resource():
    analyzer = CounterfactualAnalyzer()
    unsat_core = ["t_req_claim-3", "t_clinics_claim-3"]
    cf = analyzer.generate_z3_counterfactual(unsat_core)
    assert "If required_patients <=" in cf
    assert "SAT" in cf

def test_z3_counterfactual_unknown():
    analyzer = CounterfactualAnalyzer()
    unsat_core = ["unknown_constraint"]
    cf = analyzer.generate_z3_counterfactual(unsat_core)
    assert "If constraints unknown_constraint are relaxed, Result: SAT" in cf
