import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.verification.verification_engine import FormalVerificationEngine


def test_4_level_verification():
    print("Testing 4-Level Formal Verification Engine...")
    
    engine = FormalVerificationEngine(world_model="dummy_kg")
    
    # Base valid protocol
    valid_protocol = {
        "sampleSize": {"n_per_group": 100, "significance_level_alpha": 0.05, "target_power": 0.8}, # requires ~63, 100 is enough
        "controls": ["control arm"],
        "methodology_text": "A randomized, blinded study.",
        "assumptions": ["Gene X is active"]
    }
    
    res = engine.run(valid_protocol)
    assert res["status"] == "PASS", f"Expected PASS, got {res}"
    
    # Level 1 Failure (Statistical)
    invalid_stat_protocol = valid_protocol.copy()
    invalid_stat_protocol["sampleSize"] = {"n_per_group": 10, "significance_level_alpha": 0.05, "target_power": 0.8} # 10 < 63
    res_l1 = engine.run(invalid_stat_protocol)
    assert res_l1["status"] == "FAILED"
    assert "sample size" in res_l1["blocking_reason"].lower()
    
    # Level 2 Failure (Constraint)
    invalid_constraint_protocol = valid_protocol.copy()
    invalid_constraint_protocol["methodology_text"] = "A human clinical trial without blinding."
    res_l2 = engine.run(invalid_constraint_protocol)
    assert res_l2["status"] == "FAILED"
    assert "randomization" in res_l2["blocking_reason"].lower() or "blinding" in res_l2["blocking_reason"].lower()
    
    # Level 3 Failure (Domain)
    invalid_domain_protocol = valid_protocol.copy()
    invalid_domain_protocol["methodology_text"] = "A randomized, blinded human clinical trial with a vehicle control group."
    invalid_domain_protocol["controls"] = ["vehicle control"]
    res_l3 = engine.run(invalid_domain_protocol)
    assert res_l3["status"] == "FAILED"
    assert "vehicle" in res_l3["blocking_reason"].lower()
    
    # Level 4 Failure (Assumption)
    invalid_assumption_protocol = valid_protocol.copy()
    invalid_assumption_protocol["assumptions"] = ["This assumption is CONTRADICTED by the KG"]
    res_l4 = engine.run(invalid_assumption_protocol)
    assert res_l4["status"] == "FAILED"
    assert "contradicted" in res_l4["blocking_reason"].lower()

    print("All 4 levels successfully caught their targeted failures!")
    
if __name__ == "__main__":
    test_4_level_verification()
