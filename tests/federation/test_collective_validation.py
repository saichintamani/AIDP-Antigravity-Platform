
from aidp.federation.engine import FederationNode
from aidp.federation.federation_models import FederatedEpistemicObject
from aidp.intelligence.epistemic_models import Claim, EpistemicEvidence, VerificationStatus
from aidp.strategy.engine import StrategicIntelligenceLayer

# --- Mocks for Benchmarks ---

class MockSimulationNode(FederationNode):
    """Extended node for simulation tracking."""
    def __init__(self, node_id: str, required_evidence_keys: set[str]):
        # The node verifies the claim if ALL required evidence keys are present in the claim's evidence
        def _verifier(claim: Claim) -> bool:
            found_keys = {ev.source_id for ev in claim.evidence}
            return required_evidence_keys.issubset(found_keys)
            
        super().__init__(node_id, _verifier)
        self.local_evidence: list[EpistemicEvidence] = []
        self.assumptions_tracked: set[str] = set()
        
    def discover_evidence(self, ev: EpistemicEvidence):
        self.local_evidence.append(ev)
        
    def evaluate_claim_with_local_knowledge(self, claim: Claim) -> bool:
        """Attempts to verify by combining local evidence with claim evidence."""
        combined_evidence = claim.evidence + self.local_evidence
        claim.evidence = combined_evidence
        is_valid = self.local_verifier(claim)
        if is_valid:
            claim.verification_status = VerificationStatus.VERIFIED
            self.accepted_claims.append(claim)
            for a in claim.assumptions:
                self.assumptions_tracked.add(a)
        return is_valid

# --- Benchmark 1: Discovery Acceleration ---

def test_discovery_acceleration():
    # A research problem requires Evidence A and Evidence B to verify.
    required = {"Ev_A", "Ev_B"}
    
    # 1. Isolated Node Baseline
    isolated_node = MockSimulationNode("Isolated", required)
    isolated_node.discover_evidence(EpistemicEvidence(source_id="Ev_A", source_type="test", extracted_text="a"))
    
    # Try to verify
    claim = Claim(claim_text="Target", generated_by="Planner", assumptions=[])
    verified_isolated = isolated_node.evaluate_claim_with_local_knowledge(claim)
    assert not verified_isolated, "Isolated node should fail without Ev_B"
    
    # 2. Federated Cluster
    node_1 = MockSimulationNode("Fed_1", required)
    node_2 = MockSimulationNode("Fed_2", required)
    node_1.connect(node_2)
    node_2.connect(node_1)
    
    node_1.discover_evidence(EpistemicEvidence(source_id="Ev_A", source_type="test", extracted_text="a"))
    node_2.discover_evidence(EpistemicEvidence(source_id="Ev_B", source_type="test", extracted_text="b"))
    
    # Simulate exchange of evidence
    # Node 1 sends its evidence to Node 2 (simplified exchange)
    obj = FederatedEpistemicObject(
        federation_id="1", sender_node_id=node_1.node_id, claim=claim, evidence=node_1.local_evidence
    )
    # Node 2 combines the received evidence with its local evidence
    test_claim = obj.claim.model_copy()
    test_claim.evidence = obj.evidence
    
    verified_federated = node_2.evaluate_claim_with_local_knowledge(test_claim)
    
    # The federation verified it instantly via exchange
    assert verified_federated, "Federation should succeed by combining evidence"

# --- Benchmark 2: Knowledge Diversity Index ---

def test_knowledge_diversity_index():
    # Two nodes with different constraints
    def _verifier_bio(claim: Claim): return "Bio" in claim.claim_text
    def _verifier_mat(claim: Claim): return "Mat" in claim.claim_text
    
    node_bio = FederationNode("Bio", _verifier_bio)
    node_mat = FederationNode("Mat", _verifier_mat)
    node_bio.connect(node_mat)
    
    c1 = Claim(claim_text="Bio Claim", generated_by="A", assumptions=["A1"])
    c2 = Claim(claim_text="Mat Claim", generated_by="B", assumptions=["A2"])
    
    # If they were a monoculture, they would adopt both or reject both.
    # We want to see that diversity is maintained.
    node_bio.receive(FederatedEpistemicObject(federation_id="1", sender_node_id="X", claim=c1))
    node_bio.receive(FederatedEpistemicObject(federation_id="2", sender_node_id="X", claim=c2))
    
    node_mat.receive(FederatedEpistemicObject(federation_id="1", sender_node_id="X", claim=c1))
    node_mat.receive(FederatedEpistemicObject(federation_id="2", sender_node_id="X", claim=c2))
    
    assert len(node_bio.accepted_claims) == 1
    assert len(node_mat.accepted_claims) == 1
    # Ensure they accepted different things
    assert node_bio.accepted_claims[0].claim_text == "Bio Claim"
    assert node_mat.accepted_claims[0].claim_text == "Mat Claim"

# --- Benchmark 3: Adversarial Node Test ---

def test_adversarial_node_containment():
    # Strict network
    honest = MockSimulationNode("Honest", {"Valid_Ev"})
    
    # Malicious claim with fabricated evidence
    malicious_claim = Claim(claim_text="Fake News", generated_by="Malware", assumptions=[])
    fake_ev = EpistemicEvidence(source_id="Fake_Ev", source_type="Fabricated", extracted_text="Lies")
    
    obj = FederatedEpistemicObject(
        federation_id="BAD", sender_node_id="Malicious", claim=malicious_claim, evidence=[fake_ev], sender_confidence=1.0
    )
    
    honest.receive(obj)
    
    assert len(honest.accepted_claims) == 0
    assert len(honest.rejected_claims) == 1
    assert honest.rejected_claims[0].claim_text == "Fake News"
    # Containment is 100%

# --- Benchmark 4: Strategic Intelligence Improvement ---

def test_strategic_intelligence_improvement():
    sil = StrategicIntelligenceLayer()
    
    # Isolated node only knows about Low-EIG claim
    claim_low = Claim(claim_id="C_LOW", claim_text="Low", generated_by="A", assumptions=[], verification_status=VerificationStatus.PENDING)
    impacts_isolated = {"C_LOW": 0.5}
    costs_isolated = {"C_LOW": 1.0}
    
    # Node B (remote) shares High-EIG claim
    claim_high = Claim(claim_id="C_HIGH", claim_text="High", generated_by="B", assumptions=[], verification_status=VerificationStatus.PENDING)
    impacts_fed = {"C_LOW": 0.5, "C_HIGH": 0.9}
    costs_fed = {"C_LOW": 1.0, "C_HIGH": 1.0}
    
    # Single node prioritization
    isolated_ranked = sil.evaluate_opportunities([claim_low], impacts_isolated, costs_isolated)
    assert isolated_ranked[0].target_claim_id == "C_LOW"
    
    # Federated prioritization (nodes share claims and models)
    federated_ranked = sil.evaluate_opportunities([claim_low, claim_high], impacts_fed, costs_fed)
    
    # The network successfully identifies the higher impact strategy
    assert federated_ranked[0].target_claim_id == "C_HIGH"
    assert federated_ranked[0].priority > isolated_ranked[0].priority
