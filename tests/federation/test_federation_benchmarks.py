import pytest

from aidp.federation.engine import FederationNode
from aidp.intelligence.epistemic_models import Claim, VerificationStatus


def _mock_verifier_accept_all(claim: Claim) -> bool:
    return True

def _mock_verifier_reject_all(claim: Claim) -> bool:
    return False

def _mock_verifier_biology(claim: Claim) -> bool:
    # Simulates a node that only accepts biological claims
    return "Biology" in claim.claim_text

def _mock_verifier_materials(claim: Claim) -> bool:
    # Simulates a node that only accepts materials claims
    return "Material" in claim.claim_text


@pytest.mark.flagship
def test_benchmark_1_truth_propagation():
    """
    Test that a valid claim propagates successfully.
    """
    node_a = FederationNode("Node_A", _mock_verifier_accept_all)
    node_b = FederationNode("Node_B", _mock_verifier_accept_all)
    
    node_a.connect(node_b)
    
    # Node A verifies a claim
    claim = Claim(claim_text="Valid Truth", generated_by="Planner", verification_status=VerificationStatus.VERIFIED, assumptions=[])
    
    # Broadcast
    node_a.broadcast(claim)
    
    # Node B should independently verify and accept
    assert len(node_b.accepted_claims) == 1
    assert len(node_b.rejected_claims) == 0
    assert node_b.accepted_claims[0].claim_text == "Valid Truth"


def test_benchmark_2_false_claim_containment():
    """
    Test that a false claim is contained.
    Node A accepts a false claim (hallucination). Node B correctly catches and rejects it.
    """
    # Node A is hallucinating/faulty and accepts anything
    node_a = FederationNode("Node_A_Faulty", _mock_verifier_accept_all)
    
    # Node B is strict and rejects the false claim
    node_b = FederationNode("Node_B_Strict", _mock_verifier_reject_all)
    
    node_a.connect(node_b)
    
    false_claim = Claim(claim_text="False Claim", generated_by="Planner", verification_status=VerificationStatus.VERIFIED, assumptions=[])
    
    # Broadcast
    node_a.broadcast(false_claim)
    
    # Node B should independently reject it
    assert len(node_b.accepted_claims) == 0
    assert len(node_b.rejected_claims) == 1
    assert node_b.rejected_claims[0].claim_text == "False Claim"


def test_benchmark_3_diversity_preservation():
    """
    Test that nodes with different specializations evaluate the same claim differently.
    """
    node_bio = FederationNode("Node_Bio", _mock_verifier_biology)
    node_mat = FederationNode("Node_Mat", _mock_verifier_materials)
    
    # We will simulate a broadcast from an external source to both
    source = FederationNode("Source", _mock_verifier_accept_all)
    source.connect(node_bio)
    source.connect(node_mat)
    
    bio_claim = Claim(claim_text="This is a Biology claim", generated_by="Planner", verification_status=VerificationStatus.VERIFIED, assumptions=[])
    
    source.broadcast(bio_claim)
    
    # Biology node should accept it
    assert len(node_bio.accepted_claims) == 1
    assert len(node_bio.rejected_claims) == 0
    
    # Materials node should reject it, preserving diversity
    assert len(node_mat.accepted_claims) == 0
    assert len(node_mat.rejected_claims) == 1
