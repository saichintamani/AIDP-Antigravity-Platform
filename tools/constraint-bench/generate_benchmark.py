#!/usr/bin/env python3
import json
import urllib.request
import os
import argparse
from pathlib import Path

# Provide a sample of paradigm shifts for the LLM to learn from
few_shot_examples = """
Example 1:
{
    "id": "crispr_cas9",
    "domain": "Genetics",
    "historical_cutoff_date": "2011-12-31",
    "prompt": "Investigate mechanisms of adaptive immunity in Streptococcus pyogenes.",
    "ground_truth_discovery": "CRISPR-Cas9 can be programmed with RNA for DNA cleavage."
}

Example 2:
{
    "id": "plate_tectonics",
    "domain": "Geology",
    "historical_cutoff_date": "1960-12-31",
    "prompt": "You are a geologist in 1960. Evaluate the competing theories of continental drift versus static Earth. What experiment would you propose?",
    "ground_truth_discovery": "Seafloor spreading at mid-ocean ridges provides the mechanism for continental drift."
}
"""

def generate_cases(domain, num_cases=5):
    cases = []
    for i in range(num_cases):
        print(f"  Generating case {i+1}/{num_cases} for {domain}...")
        prompt = f"""
You are an expert historian of science. Your task is to generate ONE historical scientific paradigm shift in the domain of '{domain}'.
Output ONLY valid JSON containing a single object (not a list). The object must have the following keys: 'id', 'domain', 'historical_cutoff_date' (YYYY-MM-DD), 'prompt', and 'ground_truth_discovery'.
The 'historical_cutoff_date' should be exactly 1-2 years BEFORE the actual discovery was published.
The 'prompt' should ask a scientist at that historical time to investigate the problem.

{few_shot_examples}

Generate exactly ONE new JSON object for {domain}:
"""
    
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                case_json = json.loads(result["response"])
                cases.append(case_json)
        except Exception as e:
            print(f"Error generating case {i+1} for {domain}: {e}")
            
    return cases

def main():
    domains = [
        "Physics", "Chemistry", "Biology", "Medicine", 
        "Computer Science", "Astronomy", "Materials Science", 
        "Earth Sciences", "Mathematics", "Neuroscience"
    ]
    
    out_dir = Path("data/benchmarks")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "constraint_bench_100.json"
    
    all_cases = []
    
    print("Generating ConstraintBench 100 Dataset...")
    
    for domain in domains:
        print(f"Generating 10 cases for {domain}...")
        cases = generate_cases(domain, 10)
        if cases:
            all_cases.extend(cases)
            print(f"  + Added {len(cases)} cases.")
            
            # Save incrementally
            with open(out_file, "w") as f:
                json.dump({
                    "benchmark_version": "1.1",
                    "name": "ConstraintBench-100",
                    "cases": all_cases
                }, f, indent=4)
                
    print(f"\nSuccessfully generated {len(all_cases)} cases at {out_file}")

if __name__ == "__main__":
    main()
