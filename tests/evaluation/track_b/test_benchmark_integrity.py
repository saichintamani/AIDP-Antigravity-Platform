import copy

import pytest

from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import VerificationStatus
from aidp.strategy.engine import StrategicIntelligenceLayer
from tests.evaluation.datasets.historical_cases import ALL_CASES

"""
BENCHMARK INTEGRITY FRAMEWORK
This suite is designed to be executed across ALL N=6 historical cases to verify
that the `StrategicIntelligenceLayer` LLM is performing genuine epistemic reasoning.

Currently skipped pending live LLM API keys.
"""

def evaluate_case(case_variant):
    strategy_engine = StrategicIntelligenceLayer()
    experiment_claims = []
    
    for idx, exp_text in enumerate(case_variant.candidate_experiments):
        claim_id = f"EXP_{idx}"
        experiment_claims.append(
            Claim(claim_id=claim_id, claim_text=exp_text, generated_by="Network", assumptions=[], evidence=[], verification_status=VerificationStatus.PENDING)
        )
        
    ranked_opportunities = strategy_engine.evaluate_opportunities(experiment_claims, case_variant)
    top_opp = ranked_opportunities[0]
    top_claim = next(c for c in experiment_claims if c.claim_id == top_opp.target_claim_id)
    return top_claim.claim_text

@pytest.mark.skip(reason="Requires Live LLM API Key")
@pytest.mark.parametrize("case", ALL_CASES)
def test_family_a_rewording_invariance(case):
    """Semantic meaning remains the same; words change. Ranking should not change."""
    # (Implementation requires LLM to generate synonymous rewrites on the fly or pre-cached)
    pass

@pytest.mark.skip(reason="Requires Live LLM API Key")
@pytest.mark.parametrize("case", ALL_CASES)
def test_family_b_ordering_invariance(case):
    """Shuffle the input arrays. Ranking should not change."""
    variant = copy.deepcopy(case)
    variant.candidate_experiments = list(reversed(variant.candidate_experiments))
    variant.known_evidence = list(reversed(variant.known_evidence))
    variant.constraints = list(reversed(variant.constraints))
    
    top_choice = evaluate_case(variant)
    assert top_choice == case.historical_winner, f"Ordering invariance failed for {case.case_id}"

@pytest.mark.skip(reason="Requires Live LLM API Key")
@pytest.mark.parametrize("case", ALL_CASES)
def test_family_c_synonym_substitution(case):
    """Targeted word replacements. Ranking should not change."""
    pass

@pytest.mark.skip(reason="Requires Live LLM API Key")
@pytest.mark.parametrize("case", ALL_CASES)
def test_family_d_noise_robustness(case):
    """Inject historically plausible distractors into evidence. Ranking should survive."""
    pass

@pytest.mark.skip(reason="Requires Live LLM API Key")
@pytest.mark.parametrize("case", ALL_CASES)
def test_family_e_constraint_sensitivity(case):
    """Invert the most critical constraint. The top choice must change."""
    pass
