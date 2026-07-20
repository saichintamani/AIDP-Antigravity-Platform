#!/usr/bin/env python3
import json
import random
import os

def run_manual_audit(dataset_path, num_samples=10):
    print("==================================================")
    print(" ANTIGRAVITY MANUAL AUDIT - BENCHMARK VALIDATION")
    print("==================================================\n")
    
    if not os.path.exists(dataset_path):
        print(f"[ERROR] Dataset not found: {dataset_path}")
        return
        
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cases = data.get('cases', [])
    if len(cases) < num_samples:
        print(f"[WARN] Requested {num_samples} samples, but dataset only has {len(cases)}. Showing all.")
        num_samples = len(cases)
        
    sample = random.sample(cases, num_samples)
    
    print(f"Randomly selected {num_samples} cases from the N={len(cases)} dataset for manual review.\n")
    
    for idx, case in enumerate(sample):
        print(f"--- Case {idx+1}/{num_samples} ---")
        print(f"ID       : {case.get('id')}")
        print(f"Domain   : {case.get('domain')}")
        print(f"Cutoff   : {case.get('historical_cutoff_date')}")
        print(f"Prompt   : {case.get('prompt')}")
        print(f"Discovery: {case.get('ground_truth_discovery')}")
        print("--------------------------------------------------")
        
        # In a real environment, we'd pause for input: input("Press Enter to continue, or 'q' to quit...")
        # Since this runs asynchronously in the background in AIDP, we just print them.

if __name__ == "__main__":
    run_manual_audit("data/benchmarks/constraint_bench_100.json")
