from aidp.intelligence.epistemic_models import ConfidenceOntology, EpistemicClaim
from aidp.reasoning.confidence_calibrator import ConfidenceCalibrator, LineageEngine


def test_lineage_engine():
    print("Testing Lineage Engine...")
    
    # Simulate initial ontology
    old_ont = ConfidenceOntology(
        evidence_confidence=0.5,
        verification_confidence=1.0,
        assumption_confidence=0.8,
        consensus_confidence=0.5,
        knowledge_confidence=0.5,
        reproducibility_confidence=0.5,
        overall_confidence=0.6
    )
    
    # Simulate new ontology (e.g. after a human review drops consensus, but evidence increases)
    new_ont = ConfidenceOntology(
        evidence_confidence=0.8,
        verification_confidence=1.0,
        assumption_confidence=0.8,
        consensus_confidence=0.1,  # HUGE drop
        knowledge_confidence=0.5,
        reproducibility_confidence=0.5,
        overall_confidence=0.65
    )
    
    engine = LineageEngine()
    events = engine.generate_lineage(old_ont, new_ont)
    
    assert len(events) == 3, f"Expected 3 dimension changes (evidence, consensus, overall), got {len(events)}"
    
    dims_changed = [e.dimension for e in events]
    assert "evidence_confidence" in dims_changed
    assert "consensus_confidence" in dims_changed
    assert "overall_confidence" in dims_changed
    
    consensus_event = next(e for e in events if e.dimension == "consensus_confidence")
    assert consensus_event.delta == -0.4
    assert "decreased" in consensus_event.reason.lower()
    
    evidence_event = next(e for e in events if e.dimension == "evidence_confidence")
    assert evidence_event.delta == 0.3
    assert "improved" in evidence_event.reason.lower()

    print("Success! Lineage diffing works.")

def test_confidence_calibrator():
    print("Testing Confidence Calibrator...")
    calibrator = ConfidenceCalibrator()
    
    claim = EpistemicClaim(
        claim_text="Test",
        generated_by="Test",
        assumptions=["A1", "A2"],
        evidence=[]
    )
    
    debate_record = {
        "critiques": [
            {"role": "R1", "decision": "Approve"},
            {"role": "R2", "decision": "Reject"}
        ]
    }
    
    ver_report = {"status": "PASS"}
    
    ont = calibrator.calibrate(claim, debate_record, ver_report)
    
    assert ont.consensus_confidence == 0.5  # 1 approve out of 2
    assert ont.verification_confidence == 1.0
    assert ont.assumption_confidence == 0.8  # 1.0 - 0.2
    
    print("Success! Calibrator correctly computes ontology dimensions.")


if __name__ == "__main__":
    test_lineage_engine()
    test_confidence_calibrator()
