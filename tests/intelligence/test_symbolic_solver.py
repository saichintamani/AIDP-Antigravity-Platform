import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.intelligence.epistemic_models import Claim
from aidp.intelligence.symbolic_solver import ConstraintIntelligenceEngine
from aidp.verification.verification_engine import FormalVerificationEngine


@pytest.mark.flagship
def test_constraint_intelligence_unsat_temporal():
    engine = ConstraintIntelligenceEngine()
    
    claims = [
        Claim(
            claim_text="Enrollment at 12",
            assumptions=[],
            symbolic_formulation={"type": "temporal_event", "event": "Enrollment", "time": 12},
            generated_by="test"
        ),
        Claim(
            claim_text="OutcomeMeasurement at 6",
            assumptions=[],
            symbolic_formulation={"type": "temporal_event", "event": "OutcomeMeasurement", "time": 6},
            generated_by="test"
        ),
        Claim(
            claim_text="Enrollment before OutcomeMeasurement",
            assumptions=[],
            symbolic_formulation={"type": "temporal_order", "prior": "Enrollment", "subsequent": "OutcomeMeasurement"},
            generated_by="test"
        )
    ]
    
    proof = engine.evaluate_claims(claims)
    
    assert proof.is_valid is False
    assert "UNSAT" in proof.message
    # Assert that it correctly extracts the conflicting claims
    assert len(proof.conflicting_claim_ids) > 0

def test_constraint_intelligence_unsat_resource():
    engine = ConstraintIntelligenceEngine()
    
    claims = [
        Claim(
            claim_text="Impossible Resource Requirement",
            assumptions=[],
            symbolic_formulation={
                "type": "resource_capacity", 
                "required_patients": 10000, 
                "total_clinics": 5, 
                "patients_per_clinic": 20
            },
            generated_by="test"
        )
    ]
    
    proof = engine.evaluate_claims(claims)
    
    assert proof.is_valid is False
    assert "UNSAT" in proof.message

def test_constraint_intelligence_sat_protocol():
    engine = ConstraintIntelligenceEngine()
    
    claims = [
        Claim(
            claim_text="Valid Protocol Logic",
            assumptions=[],
            symbolic_formulation={
                "type": "protocol_logic", 
                "has_control": True, 
                "power": 0.90
            },
            generated_by="test"
        )
    ]
    
    proof = engine.evaluate_claims(claims)
    assert proof.is_valid is True
    assert "SAT" in proof.message

def test_verification_engine_integration():
    # Test that the FormalVerificationEngine correctly translates the protocol into claims
    engine = FormalVerificationEngine(world_model=None)
    
    protocol = {
        "design": {"has_control_group": True},
        "controls": ["placebo"],
        "statistical_power": 0.85,
        "sampleSize": {"n_per_group": 1000},
        "patients": 1000,
        "total_clinics": 2,
        "patients_per_clinic": 10
    }
    
    report = engine.run(protocol)
    
    assert report["status"] == "FAILED"
    assert "Symbolic Proof FAILED: UNSAT" in report["blocking_reason"]
