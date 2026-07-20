import os
import subprocess
import sys

def run_suite(suite_name, command):
    print(f"\n==================================================")
    print(f"Executing: {suite_name}")
    print(f"Command: {command}")
    print(f"==================================================")
    
    # We use pytest directly to ensure we capture the return code
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
        
    if result.returncode == 0:
        print(f"\n[SUCCESS] {suite_name} completed without errors.")
    else:
        print(f"\n[FAILURE] {suite_name} failed. (This may be expected for the Failure Suite)")
    return result.returncode

def main():
    print("AIDP Reproducibility Script")
    print("Initializing Phase 11 validation...")
    
    # 1. Structural Validation (Phase 9)
    run_suite("Structural Reasoning Logic", "pytest tests/test_formal_verification.py tests/test_domain_routing_accuracy.py tests/test_debate_adversarial_strength.py tests/test_ledger_immutability.py")
    
    # 2. Empirical Measurement (Phase 10)
    # Note: We specify the exact 3 benchmark files to avoid the sentence-transformers protobuf error on other benchmark files.
    run_suite("Empirical Capability Benchmarks", "pytest tests/benchmarks/test_cross_domain_robustness.py tests/benchmarks/test_ablations.py tests/benchmarks/test_confidence_calibration.py")
    
    # 3. Known Limitations (Phase 11)
    print("\nRunning Failure Reproduction Suite...")
    print("Note: These tests are marked with @pytest.mark.xfail. If they PASS pytest (showing xfail), it means the known limitation successfully reproduced.")
    run_suite("Known Architecture Failures", "pytest tests/failures/test_known_limitations.py")
    
    print("\n==================================================")
    print("Reproduction Run Complete.")
    print("Please cross-reference results with CAPABILITY_REPRODUCTION_REPORT.md.")
    
if __name__ == "__main__":
    main()
