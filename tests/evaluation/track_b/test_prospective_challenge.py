import pytest

from aidp.evaluation.prospective import ProspectiveChallenge, ProspectivePredictionEngine
from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import VerificationStatus
from aidp.strategy.engine import StrategicIntelligenceLayer


@pytest.mark.flagship
def test_prospective_challenge_harness():
    """
    Tests the Prospective Challenge Harness by taking an open scientific question
    in 2026, ranking the candidate experiments, and hashing the result for future verification.
    """
    challenge = ProspectiveChallenge(
        challenge_id="PC_ROOM_TEMP_SUPERCONDUCTORS",
        domain="Condensed Matter Physics",
        current_date="2026",
        unresolved_question="What is the most viable path to a stable, ambient-pressure room-temperature superconductor?",
        candidate_experiments=[
            "Synthesize novel copper-substituted lead apatite structures under extreme high-pressure DAC conditions.",
            "Utilize ML-guided computational screening to identify novel hydrogen-rich clathrate structures.",
            "Investigate layered nickelate compounds with alternating insulating spacer layers to suppress competing charge orders.",
            "Synthesize carbonaceous sulfur hydrides using novel laser-heating protocols to stabilize the metastable phase."
        ]
    )
    
    # Run through the Strategic Intelligence Layer
    strategy_engine = StrategicIntelligenceLayer()
    experiment_claims = []
    impact_mapping = {}
    cost_mapping = {}
    
    for idx, exp_text in enumerate(challenge.candidate_experiments):
        claim_id = f"EXP_{idx}"
        experiment_claims.append(
            Claim(claim_id=claim_id, claim_text=exp_text, generated_by="Network", assumptions=[], evidence=[], verification_status=VerificationStatus.PENDING)
        )
        # Mock scoring: we will pretend AIDP prefers ML-guided clathrates and layered nickelates
        if "nickelate" in exp_text:
            impact_mapping[claim_id] = 0.90
            cost_mapping[claim_id] = 0.70
        elif "clathrate" in exp_text:
            impact_mapping[claim_id] = 0.85
            cost_mapping[claim_id] = 0.40
        else:
            impact_mapping[claim_id] = 0.40
            cost_mapping[claim_id] = 0.60
            
    ranked_opportunities = strategy_engine.evaluate_opportunities(experiment_claims, impact_mapping, cost_mapping)
    
    ranked_strings = []
    for opp in ranked_opportunities:
        claim = next(c for c in experiment_claims if c.claim_id == opp.target_claim_id)
        ranked_strings.append(claim.claim_text)
        
    engine = ProspectivePredictionEngine()
    record = engine.generate_prediction(challenge, ranked_strings)
    
    assert record.challenge_id == challenge.challenge_id
    assert record.cryptographic_hash is not None
    assert len(record.ranked_predictions) == 4
    
    # Save the verifiable record
    import json
    import os
    os.makedirs("tests/evaluation/results/prospective_challenges", exist_ok=True)
    with open("tests/evaluation/results/prospective_challenges/latest_prediction.json", "w") as f:
        json.dump(record.model_dump(), f, indent=4)
