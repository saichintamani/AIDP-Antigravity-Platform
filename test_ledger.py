import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from aidp.platform.epistemic_logger import EpistemicLedger
from aidp.intelligence.epistemic_models import EpistemicClaim, EpistemicEvidence, EpistemicReview, VerificationStatus

ledger = EpistemicLedger(filepath="data/test_ledger.jsonl")

claim = EpistemicClaim(
    claim_text="Test Claim",
    evidence=[EpistemicEvidence(source_id="1", source_type="lit", extracted_text="text", relevance_score=1.0)],
    assumptions=["Assumed true"],
    generated_by="Test",
)

ledger.append_claim(claim)

claim.reviewed_by = [EpistemicReview(reviewer_role="Statistician", vote="approve", rationale="Good", identified_confounds=[])]
claim.confidence_score = 1.0
claim.verification_status = VerificationStatus.VERIFIED

ledger.append_claim(claim)

claims = ledger.get_all_claims()
print(f"Loaded {len(claims)} claims.")
for c in claims:
    print(c.claim_id, c.verification_status, len(c.reviewed_by))
