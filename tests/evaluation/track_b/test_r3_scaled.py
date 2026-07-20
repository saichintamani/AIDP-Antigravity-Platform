import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from aidp.evaluation.scaled_runner import ScaledDiscoveryRunner

def test_r3_scaled_runner_mock():
    print("\n--- Testing R3 Scaled Runner (MOCK MODE) ---")
    runner = ScaledDiscoveryRunner(use_mock=True)
    
    # Mock the underlying harness to prevent real LLM calls
    runner.harness.generate_hypothesis = lambda case: {
        "status": "success",
        "generated_hypothesis": "This is a mocked hypothesis that should pass deterministic checks because it is long enough. 40 angstroms.",
        "retries_used": 0
    }
    
    # Use an in-memory output path for testing or a temp file
    output_path = os.path.join(os.path.dirname(__file__), '../results/test_r3_scaled_mock.json')
    
    results = runner.run_all(output_path=output_path)
    
    # Assertions
    assert len(results) == 10, f"Expected 10 results, got {len(results)}"
    
    successes = [r for r in results if r["status"] == "success"]
    assert len(successes) == 10, "Not all cases succeeded in mock mode"
    
    # Check structure
    sample = successes[0]
    assert "judge_verdict" in sample
    assert "constraints_report" in sample
    assert "scientific_grounding" in sample["judge_verdict"]
    
    print("[PASS] R3 Scaled Runner tests passed!")

if __name__ == "__main__":
    test_r3_scaled_runner_mock()
