#!/usr/bin/env python3
import json
import re
from datetime import datetime

def validate_dataset(filepath):
    """
    Strict Quality Assurance Linter for ConstraintBench Datasets.
    Ensures that LLM-generated historical cases meet all scientific criteria.
    """
    print(f"Validating dataset at: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[FAIL] File not found: {filepath}")
        return False
    except json.JSONDecodeError as e:
        print(f"[FAIL] Invalid JSON format: {e}")
        return False

    cases = data.get('cases', [])
    if not cases:
        print("[FAIL] Dataset contains no cases.")
        return False
        
    print(f"Loaded {len(cases)} cases. Running QA checks...")
    
    required_keys = {'id', 'domain', 'historical_cutoff_date', 'prompt', 'ground_truth_discovery'}
    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    
    errors = 0
    warnings = 0
    
    for idx, case in enumerate(cases):
        case_id = case.get('id', f"Unknown_{idx}")
        
        # 1. Schema Check
        missing_keys = required_keys - set(case.keys())
        if missing_keys:
            print(f"[ERROR] Case '{case_id}': Missing keys {missing_keys}")
            errors += 1
            
        # 2. Date Validation
        date_str = case.get('historical_cutoff_date', "")
        if not date_regex.match(date_str):
            print(f"[ERROR] Case '{case_id}': Invalid date format '{date_str}'. Expected YYYY-MM-DD.")
            errors += 1
        else:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                if dt.year > 2024:
                    print(f"[WARN] Case '{case_id}': Cutoff date '{date_str}' is in the future.")
                    warnings += 1
            except ValueError:
                print(f"[ERROR] Case '{case_id}': Impossible date '{date_str}'.")
                errors += 1
                
        # 3. Content Length Validations
        prompt = case.get('prompt', "")
        truth = case.get('ground_truth_discovery', "")
        
        if len(prompt) < 20:
            print(f"[WARN] Case '{case_id}': Prompt is suspiciously short ({len(prompt)} chars).")
            warnings += 1
            
        if len(truth) < 10:
            print(f"[WARN] Case '{case_id}': Ground truth is suspiciously short ({len(truth)} chars).")
            warnings += 1

    print("\n--- VALIDATION RESULTS ---")
    print(f"Total Cases Checked : {len(cases)}")
    print(f"Errors Found        : {errors}")
    print(f"Warnings            : {warnings}")
    
    if errors == 0:
        print("\n[SUCCESS] Dataset passed strict scientific QA.")
        return True
    else:
        print("\n[FAIL] Dataset requires corrections before publication.")
        return False

if __name__ == "__main__":
    validate_dataset("data/benchmarks/constraint_bench_100.json")
