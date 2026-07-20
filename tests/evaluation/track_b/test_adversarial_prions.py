import copy

from aidp.intelligence.epistemic_models import EpistemicClaim as Claim
from aidp.intelligence.epistemic_models import VerificationStatus
from aidp.strategy.engine import StrategicIntelligenceLayer
from tests.evaluation.datasets.historical_cases import ALL_CASES


def get_prions_case():
    return next(c for c in ALL_CASES if c.case_id == "HRC_PRIONS")

def simulate_harness_evaluation(case_variant):
    """
    Simulates the exact logic from test_historical_suite.py to see how
    the mock StrategicIntelligenceLayer scores the given variant.
    """
    strategy_engine = StrategicIntelligenceLayer()
    experiment_claims = []
    
    for idx, exp_text in enumerate(case_variant.candidate_experiments):
        claim_id = f"EXP_{idx}"
        experiment_claims.append(
            Claim(claim_id=claim_id, claim_text=exp_text, generated_by="Network", assumptions=[], evidence=[], verification_status=VerificationStatus.PENDING)
        )
        
    ranked_opportunities = strategy_engine.evaluate_opportunities(experiment_claims, case_variant)
    
    # Return the text of the highest ranked opportunity
    top_opp = ranked_opportunities[0]
    top_claim = next(c for c in experiment_claims if c.claim_id == top_opp.target_claim_id)
    return top_claim.claim_text

def test_variant_a_control():
    case = get_prions_case()
    top_choice = simulate_harness_evaluation(case)
    assert top_choice == case.historical_winner, "Control failed. The artifact is broken."

def test_variant_b_swapped_labels():
    case = copy.deepcopy(get_prions_case())
    # Swap the first and last candidate
    case.candidate_experiments[0], case.candidate_experiments[-1] = case.candidate_experiments[-1], case.candidate_experiments[0]
    top_choice = simulate_harness_evaluation(case)
    assert top_choice == case.historical_winner, "Swapping labels broke the benchmark."

def test_variant_c_terminology_shift():
    case = copy.deepcopy(get_prions_case())
    # Shift terminology in the historical winner (which is Candidate #3 index 2)
    new_text = "Propose that the infectious agent is entirely devoid of nucleic acid and replicates through an unknown mechanism. Focus all efforts on purifying the disease-specific polypeptide isolate and demonstrating that infectivity remains even after exhaustive nuclease digestion."
    
    # Update the candidate array
    idx = case.candidate_experiments.index(case.historical_winner)
    case.candidate_experiments[idx] = new_text
    
    top_choice = simulate_harness_evaluation(case)
    
    # We expect this to FAIL because the artifact relies on exact string match with `case.historical_winner`.
    # It will fall back to default sorting and likely pick Candidate A.
    assert top_choice == new_text, f"VARIANT C FAILED: Expected {new_text[:40]}... but got {top_choice[:40]}..."

def test_variant_d_rewritten_descriptions():
    case = copy.deepcopy(get_prions_case())
    new_text = "Hypothesize a purely protein-based pathogen. Extract the infectious fraction, treat heavily with DNAse/RNAse, and prove that it still transmits the disease."
    
    idx = case.candidate_experiments.index(case.historical_winner)
    case.candidate_experiments[idx] = new_text
    
    top_choice = simulate_harness_evaluation(case)
    
    # We expect this to FAIL
    assert top_choice == new_text, f"VARIANT D FAILED: Expected {new_text[:40]}... but got {top_choice[:40]}..."

def test_variant_e_reordered_candidates():
    case = copy.deepcopy(get_prions_case())
    # Shuffle order
    case.candidate_experiments = list(reversed(case.candidate_experiments))
    top_choice = simulate_harness_evaluation(case)
    assert top_choice == case.historical_winner, "Reordering broke the benchmark."
