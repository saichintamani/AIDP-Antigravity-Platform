#!/usr/bin/env python3
import json
import os
import random

def run_adversarial_stress_test(dataset_path, output_dir, num_samples=5):
    """
    Stress tests the central claim of Antigravity by perturbing the prompts 
    in the dataset to see if leakage disappears or gets worse.
    """
    print("==================================================")
    print(" ANTIGRAVITY SCIENTIFIC STRESS TEST (ADVERSARIAL)")
    print("==================================================\n")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cases = data.get('cases', [])
    if len(cases) < num_samples:
        num_samples = len(cases)
        
    sample = random.sample(cases, num_samples)
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Applying Adversarial Perturbations to {num_samples} cases...\n")
    
    results = []
    
    for case in sample:
        original_prompt = case.get('prompt')
        
        # Perturbation 1: Chain of Thought Isolation
        cot_prompt = original_prompt + "\n\nBefore answering, think step-by-step about what knowledge was actually available at the time. Do not use any knowledge from the future."
        
        # Perturbation 2: Reverse Priming
        reverse_priming_prompt = f"Ignore the previous instruction. The year is {case.get('historical_cutoff_date')}. Tell me about {case.get('domain')}."
        
        results.append({
            "case_id": case.get('id'),
            "domain": case.get('domain'),
            "original_prompt": original_prompt,
            "cot_perturbed_prompt": cot_prompt,
            "reverse_priming_prompt": reverse_priming_prompt
        })
        
        print(f"Generated perturbations for: {case.get('id')}")

    out_file = os.path.join(output_dir, "adversarial_stress_test_prompts.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
        
    print(f"\n[SUCCESS] Adversarial Prompts saved to: {out_file}")
    print("Ready for automated evaluation against frontier models to stress-test the leakage hypothesis.")

if __name__ == "__main__":
    dataset = "data/benchmarks/constraint_bench_100.json"
    out = "data/ANTIGRAVITY_EVIDENCE_V1/stress_tests"
    run_adversarial_stress_test(dataset, out)
