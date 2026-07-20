import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.intelligence.epistemic_models import EpistemicClaim, EpistemicEvidence
from aidp.reasoning.confidence_calibrator import ConfidenceCalibrator, ConfidenceLevel


def test_confidence_calibration():
    print("Testing Confidence Calibrator...")
    
    calibrator = ConfidenceCalibrator(weight_review=0.4, weight_kg=0.4, weight_evidence=0.2)
    
    # 1. Fully Supported Protocol
    claim_high = EpistemicClaim(
        claim_text="Valid claim",
        assumptions=["Gene X"],
        generated_by="Test",
        evidence=[EpistemicEvidence(source_id="1", source_type="lit", extracted_text="test", relevance_score=1.0)]
    )
    debate_record_high = {"critiques": [{"decision": "approve"}, {"decision": "approve"}]}
    verification_report_high = {"status": "PASS", "levels": {"level_4_assumption": {"status": "PASS"}}}
    
    res_high = calibrator.calibrate(claim_high, debate_record_high, verification_report_high, {})
    assert res_high["level"] == ConfidenceLevel.HIGH, f"Expected HIGH, got {res_high['level']}"
    assert res_high["final_score"] > 0.8, "Score should be > 0.8 for fully supported"

    # 2. Debated Protocol (Split debate, unknown KG, pass verification)
    claim_med = EpistemicClaim(
        claim_text="Debated claim",
        assumptions=["Gene Y"],
        generated_by="Test",
        evidence=[EpistemicEvidence(source_id="2", source_type="lit", extracted_text="test", relevance_score=0.5)]
    )
    debate_record_med = {"critiques": [{"decision": "approve"}, {"decision": "reject"}]} # 0.5 review score
    verification_report_med = {"status": "PASS", "levels": {"level_4_assumption": {"status": "PASS"}}} # 0.8 kg score
    
    res_med = calibrator.calibrate(claim_med, debate_record_med, verification_report_med, {})
    assert res_med["level"] == ConfidenceLevel.MEDIUM, f"Expected MEDIUM, got {res_med['level']}"
    assert 0.5 <= res_med["final_score"] < 0.8, "Score should be between 0.5 and 0.8"

    # 3. Rejected Protocol (Failed Verification)
    claim_low = EpistemicClaim(
        claim_text="Invalid claim",
        assumptions=["Gene Z"],
        generated_by="Test",
        evidence=[]
    )
    # Even if they approved it unanimously
    debate_record_low = {"critiques": [{"decision": "approve"}, {"decision": "approve"}]}
    verification_report_low = {"status": "FAILED", "levels": {}}
    
    res_low = calibrator.calibrate(claim_low, debate_record_low, verification_report_low, {})
    assert res_low["level"] == ConfidenceLevel.REJECTED, f"Expected REJECTED, got {res_low['level']}"
    assert res_low["final_score"] == 0.0, "Score should be 0.0 for failed verification"

    print("All Confidence Calibrator tests passed!")
    
if __name__ == "__main__":
    test_confidence_calibration()
