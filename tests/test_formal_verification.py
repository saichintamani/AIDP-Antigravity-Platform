import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.discovery.scientific_planning import FalsifiabilityValidator, StatisticalPowerAnalyzer
from aidp.verification.logic_solver import LogicSolver
from aidp.verification.statistical_solver import StatisticalSolver


def test_formal_verification():
    print("Testing Formal Verification Engine...")
    
    # 1. Statistical Solver Math
    stats_solver = StatisticalSolver()
    
    # For a large effect size (d=0.8), we expect smaller sample size
    n1 = stats_solver.compute_sample_size(effect_size=0.8, alpha=0.05, power=0.8)
    
    # For a small effect size (d=0.2), we expect much larger sample size
    n2 = stats_solver.compute_sample_size(effect_size=0.2, alpha=0.05, power=0.8)
    
    assert n2 > n1
    assert n1 == 25  # 2 * ((1.96 + 0.84) / 0.8)^2 = 2 * (2.8 / 0.8)^2 = 2 * 3.5^2 = 2 * 12.25 = 24.5 -> 25
    
    # 2. StatisticalPowerAnalyzer Integration
    analyzer = StatisticalPowerAnalyzer(planner=None) # LLM no longer needed
    stats_res = analyzer.validate(methodology={}, controls=[], failure_criteria="")
    assert "sample_size_recommendation" in stats_res
    assert stats_res["sample_size_recommendation"]["n_per_group"] == 63 # Default d=0.5 -> 2 * (2.8/0.5)^2 = 2 * 31.36 = 62.72 -> 63
    
    # 3. Logic Solver Math
    logic_solver = LogicSolver()
    
    # Missing DV
    res_missing = logic_solver.validate("X cures Y", "It works", {})
    assert "UNFALSIFIABLE" in res_missing["failure_criteria"]
    
    # Present DV
    res_valid = logic_solver.validate("Drug X reduces tumor size", "Tumor shrinks", {"dependent": ["tumor size"]})
    assert "tumor size does not significantly change" in res_valid["failure_criteria"]
    
    # 4. FalsifiabilityValidator Integration
    f_val = FalsifiabilityValidator(planner=None)
    f_res = f_val.validate("Drug X reduces tumor size", "Tumor shrinks", {"dependent": ["tumor size"]})
    assert "tumor size does not significantly change" in f_res["failure_criteria"]
    assert "tumor size does not significantly change" in f_res["failure_criteria"]
    
    # 5. FormalVerificationEngine Ontology Integration
    from aidp.verification.verification_engine import FormalVerificationEngine
    engine = FormalVerificationEngine(world_model=None)
    
    protocol = {
        "domain": "WET_LAB",
        "sampleSize": {"n_per_group": 100}, # Pass stats
        "controls": ["Mock"], # Pass domain constraints
        "assumptions": ["Assumption 1", "Assumption 2"]
    }
    
    # 6. DomainMetricValidator tests
    from aidp.planning.metrics import DomainMetricValidator
    validator = DomainMetricValidator()
    
    # Missing controls for WET_LAB
    bad_wet_lab = {"domain": "WET_LAB"}
    res = validator.validate_design(bad_wet_lab)
    assert not res["valid"]
    assert any("missing controls" in p for p in res["penalties"])
    
    # Missing comparator and randomization for CLINICAL_TRIAL
    bad_clinical = {"domain": "CLINICAL_TRIAL"}
    res = validator.validate_design(bad_clinical)
    assert not res["valid"]
    assert any("missing comparator" in p for p in res["penalties"])
    assert any("missing randomization" in p for p in res["penalties"])
    
    print("Formal Verification tests passed!")
    
    report = engine.run(protocol)
    print("Report:", report)
    
    assert "ontology" in report
    ontology = report["ontology"]
    assert ontology["verification_confidence"] == 1.0
    assert ontology["evidence_confidence"] == 1.0
    # Both assumptions are effectively untested mock fails or passes, but let's check it doesn't crash
    assert "assumption_confidence" in ontology
    
    print("Formal Verification tests passed successfully!")

if __name__ == "__main__":
    test_formal_verification()
