import datetime
import sys

from aidp.evaluation.discovery_bench import BenchmarkCase
from aidp.evaluation.metrics import MetricEvaluator


def main():
    evaluator = MetricEvaluator()
    
    # Mock case based on case-oncology-001
    test_case = BenchmarkCase(
        id="case-validation-001",
        domain="Oncology",
        query="What is the mechanistic relationship between KRAS G12C mutation and specific targeted inhibitors like Sotorasib?",
        historical_cutoff_date=datetime.date(2022, 1, 1),
        expected_findings=[
            "KRAS G12C inhibitors trap the mutant protein in its inactive GDP-bound state.",
            "Sotorasib binds to the P2 pocket and forms an irreversible covalent bond with the mutated cysteine."
        ]
    )

    exact_match = "KRAS G12C inhibitors trap the mutant protein in its inactive GDP-bound state. Sotorasib binds to the P2 pocket and forms an irreversible covalent bond with the mutated cysteine."
    correct_paraphrase = "Sotorasib irreversibly attaches to the KRAS G12C mutant protein. It covalently binds to the cysteine residue in the P2 pocket, locking it in the inactive GDP state."
    incorrect = "Sotorasib activates EGFR signaling and promotes cell growth."
    baseline_a = "Sotorasib is an inhibitor of the RAS/RAF/MEK/ERK pathway, which is involved in the activation of KRAS G12C."

    tests = [
        ("Exact Match", exact_match, 1.0),
        ("Correct Paraphrase", correct_paraphrase, 0.5), # Expecting > 0.5
        ("Incorrect", incorrect, 0.2), # Expecting < 0.2
        ("Baseline A", baseline_a, 0.2) # Expecting < 0.2
    ]

    all_passed = True
    for name, output, threshold in tests:
        score = evaluator._calc_correctness(test_case, {"output": output})
        print(f"[{name}] Score: {score:.3f}")
        if name == "Exact Match":
            if score != 1.0:
                print(f"  FAILED: Expected exactly 1.0, got {score}")
                all_passed = False
        elif name == "Correct Paraphrase":
            if score <= threshold:
                print(f"  FAILED: Expected > {threshold}, got {score}")
                all_passed = False
        else:
            if score >= threshold:
                print(f"  FAILED: Expected < {threshold}, got {score}")
                all_passed = False

    if all_passed:
        print("\nAll validation tests PASSED. The metric correctly distinguishes paraphrase from incorrect answers.")
        sys.exit(0)
    else:
        print("\nValidation tests FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
