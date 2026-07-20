import argparse
import os
from pathlib import Path

# Base directory for the project (two levels up)
base_dir = Path(__file__).parent.parent

from pathlib import Path

base_dir = Path(__file__).parent.parent


from run_live_discoverybench import load_config, load_dataset, preflight_checks


def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "scripts" / "benchmark_execution_config.yaml"
    dataset_path = base_dir / "src" / "aidp" / "evaluation" / "data" / "discovery_bench_v1.json"
    evidence_dir = base_dir / "docs" / "evaluation" / "evidence"
    
    config = load_config(str(config_path))
    dataset = load_dataset(str(dataset_path))
    
    preflight_checks(config, len(dataset), evidence_dir)
    print("All PREFLIGHT CHECKS PASSED. Launch readiness verified.")

if __name__ == "__main__":
    main()
