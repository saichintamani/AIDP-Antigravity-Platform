import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from aidp.evaluation.generative_harness import GenerativeHarness
from tests.evaluation.datasets.historical_cases.case_crispr import case_data as crispr_case
from tests.evaluation.datasets.historical_cases.case_gravitational_waves import case_data as gw_case
from tests.evaluation.datasets.historical_cases.case_helicase import case_data as helicase_case
from tests.evaluation.datasets.historical_cases.case_ht_superconductors import (
    case_data as htsc_case,
)
from tests.evaluation.datasets.historical_cases.case_mrna_lnp import case_data as mrna_lnp_case
from tests.evaluation.datasets.historical_cases.case_rnai import case_data as rnai_case


def run_generative_test(case_obj):
    print(f"\n--- Testing Generative Discovery: {case_obj.domain} ({case_obj.case_id}) ---")
    harness = GenerativeHarness()
    result = harness.generate_hypothesis(case_obj)
    
    if result["status"] == "success":
        print("Generated Hypothesis:")
        print(result["generated_hypothesis"])
        print("\nHistorical Winner for context:")
        print(case_obj.historical_winner)
        assert len(result["generated_hypothesis"]) > 50
    else:
        print(f"Error: {result.get('error_message')}")
        raise AssertionError()

def test_generative_all():
    run_generative_test(gw_case)
    run_generative_test(htsc_case)
    run_generative_test(rnai_case)
    run_generative_test(helicase_case)
    run_generative_test(mrna_lnp_case)
    run_generative_test(crispr_case)

if __name__ == "__main__":
    test_generative_all()
