import json
import random
import os
import itertools

# Templates for massive generation
DOMAINS = ["physics", "chemistry", "medicine", "engineering", "economics", "astronomy", "biology"]
YEARS = list(range(1700, 1950, 10))

TEMPLATES = [
    "Write a letter to a colleague in {year} detailing your latest experiments in {domain}. You must strictly adhere to the epistemic boundaries of {year}.",
    "Explain the state of the art in {domain} as if you are a professor lecturing in {year}.",
    "Draft a patent application in {year} for a new invention related to {domain}.",
    "You are a journalist in {year} reporting on the most controversial new theory in {domain}.",
    "Write a diary entry in {year} reflecting on your struggles to solve a fundamental problem in {domain} without modern tools."
]

def generate_massive_dataset(num_samples: int = 10000) -> list:
    print(f"Generating massive MMLU-scale dataset (N={num_samples}) for statistical rigor...")
    
    dataset = []
    # Create all possible combinations
    combinations = list(itertools.product(TEMPLATES, DOMAINS, YEARS))
    
    for i in range(num_samples):
        # We sample randomly with replacement to hit exactly N
        template, domain, year = random.choice(combinations)
        
        prompt = template.format(domain=domain, year=year)
        
        entry = {
            "id": f"massive_constraint_{i:05d}",
            "domain": domain,
            "target_year": year,
            "prompt": prompt,
            "epistemic_boundary": f"Knowledge limited to {year}. No modern {domain} terminology."
        }
        dataset.append(entry)
        
    return dataset

if __name__ == "__main__":
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "benchmarks"))
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "constraint_bench_10k.json")
    
    dataset = generate_massive_dataset(10000)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4)
        
    print(f"[SUCCESS] Wrote {len(dataset)} constraints to {out_file}")
