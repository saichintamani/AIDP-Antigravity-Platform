import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import uuid

from aidp.discovery.workflow import DiscoverySession, ReviewNode
from aidp.intelligence.epistemic_models import (
    ConfidenceOntology,
    EpistemicClaim,
    VerificationStatus,
)
from aidp.platform.epistemic_logger import EpistemicLedger


class MockPlannerForReview:
    def __init__(self, should_approve):
        self.should_approve = should_approve
        
    def execute_task(self, spec):
        if self.should_approve:
            return {
                "consensusReached": True,
                "consensusReport": "The methodology is perfectly sound.",
                "critiques": [
                    {"role": "Statistician", "decision": "approve", "evidence": "Sample size is adequate.", "blockingIssues": []},
                    {"role": "Bioethicist", "decision": "approve", "evidence": "Ethical concerns addressed.", "blockingIssues": []}
                ]
            }
        else:
            return {
                "consensusReached": False,
                "consensusReport": "The methodology is flawed due to missing placebo.",
                "critiques": [
                    {"role": "Statistician", "decision": "reject", "evidence": "Missing placebo control arm.", "blockingIssues": ["no_placebo"]},
                    {"role": "Bioethicist", "decision": "approve", "evidence": "Ethical concerns addressed.", "blockingIssues": []}
                ]
            }

def test_debate_rejects_flawed_methodology(tmp_path):
    ledger_path = tmp_path / "ledger.db"
    ledger = EpistemicLedger(db_uri=f"sqlite:///{ledger_path}")
    
    # Inject a claim into the ledger
    claim_id = str(uuid.uuid4())
    claim = EpistemicClaim(
        claim_id=claim_id,
        claim_text="Flawed claim",
        assumptions=[],
        generated_by="pytest",
        confidence=ConfidenceOntology()
    )
    ledger.append_claim(claim)
    
    # Provide a mock gateway
    class MockGateway:
        def query(self, *args, **kwargs):
            return {}
            
    node = ReviewNode(gateway=MockGateway())
    node.ledger = ledger
    class MockDebateEngine:
        def evaluate_design(self, design, hypothesis):
            return {
                "consensusReached": False,
                "consensusReport": "The methodology is flawed due to missing placebo.",
                "critiques": [
                    {"role": "Statistician", "decision": "reject", "evidence": "Missing placebo control arm.", "blockingIssues": ["no_placebo"]},
                    {"role": "Bioethicist", "decision": "approve", "evidence": "Ethical concerns addressed.", "blockingIssues": []}
                ]
            }
            
    node.debate_engine = MockDebateEngine()
    class MockCalibrator:
        def calibrate(self, *args, **kwargs):
            return ConfidenceOntology(
                evidence_confidence=0.5,
                verification_confidence=0.0,
                assumption_confidence=0.5,
                consensus_confidence=0.0,
                knowledge_confidence=0.5,
                reproducibility_confidence=0.5,
                overall_confidence=0.1
            )
    node.calibrator = MockCalibrator()
    
    session = DiscoverySession()
    session.experiment_design = {"epistemic_claim_id": claim_id}
    session.hypothesis = {"claim": "Flawed claim"}
    session.debate_record = {}
    
    # Simulate receiving the REVIEW_COMPLETED event
    # In the actual DAG, this is triggered when the planner completes. 
    # For testing, we just call the inner logic or simulate the event.
    # Actually, ReviewNode.execute calls execute_task.
    
    state = node.execute(session)
    
    assert state.name == "FAILED"
    
    # Verify the ledger updated the claim
    updated_claim = ledger.get_claim_by_id(claim_id)
    assert updated_claim.verification_status == VerificationStatus.REJECTED
    assert len(updated_claim.reviewed_by) == 2
    
    # Find statistician review
    stat_review = next(r for r in updated_claim.reviewed_by if r.reviewer_role == "Statistician")
    assert stat_review.vote == "reject"
    assert "no_placebo" in stat_review.identified_confounds
