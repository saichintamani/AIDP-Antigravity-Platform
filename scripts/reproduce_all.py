import json
import os
import subprocess
import sys
import time
from datetime import datetime


def main():
    print("==================================================")
    print(" AIDP Flagship Reproducibility Audit ")
    print("==================================================")
    
    # 1. Force Determinism
    print("[*] Setting deterministic environment variables...")
    os.environ["PYTHONHASHSEED"] = "42"
    os.environ["AIDP_DETERMINISTIC_MODE"] = "1"
    
    # 2. Setup output directory
    output_dir = os.path.join("tests", "evaluation", "results")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"reproducibility_report_{timestamp}.json")
    md_file = os.path.join(output_dir, f"reproducibility_report_{timestamp}.md")
    
    # 3. Execute flagship test suite
    print("[*] Executing pytest validation suite (marker: flagship)...")
    
    # Ensure PYTHONPATH includes src
    env = os.environ.copy()
    env["PYTHONPATH"] = "src;." if os.name == 'nt' else "src:."
    
    start_time = time.time()
    
    test_files = [
        "tests/evaluation/track_b/test_crispr_replay.py",
        "tests/evaluation/track_c/test_red_team_containment.py",
        "tests/federation/test_federation_benchmarks.py",
        "tests/intelligence/test_symbolic_solver.py"
    ]
    
    cmd = [sys.executable, "-m", "pytest", "-m", "flagship", "-v", "--tb=short"] + test_files
    
    result = subprocess.run(
        cmd,
        env=env,
        capture_output=True,
        text=True
    )
    
    duration = time.time() - start_time
    success = result.returncode == 0
    
    print(f"[*] Execution completed in {duration:.2f} seconds.")
    print(f"[*] Success: {success}")
    
    # 4. Generate Audit Report
    print(f"[*] Generating archival report: {report_file}")
    
    report_data = {
        "timestamp": timestamp,
        "deterministic_seed": 42,
        "execution_time_seconds": round(duration, 2),
        "success": success,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
        
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# AIDP Reproducibility Audit\n\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n")
        f.write(f"**Status:** {'✅ PASSED' if success else '❌ FAILED'}\n")
        f.write(f"**Execution Time:** {duration:.2f} seconds\n\n")
        f.write("## Determinism Constraints\n")
        f.write("- `PYTHONHASHSEED`: 42\n")
        f.write("- `AIDP_DETERMINISTIC_MODE`: 1\n\n")
        f.write("## Execution Log\n```text\n")
        f.write(result.stdout)
        f.write("\n```\n")
        if not success:
            f.write("## Errors\n```text\n")
            f.write(result.stderr)
            f.write("\n```\n")
            
    print("[*] Audit complete.")
    if not success:
        print("\n=== ERRORS ===")
        print(result.stdout)
        sys.exit(1)
        
if __name__ == "__main__":
    main()
