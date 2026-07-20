#!/usr/bin/env python3
import json
import os

def export_huggingface_dataset(dataset_path, output_dir):
    """
    Converts the internal constraint_bench_100.json into a standard HuggingFace 
    JSONL dataset, complete with dataset cards.
    """
    print("==================================================")
    print(" ANTIGRAVITY HUGGINGFACE EXPORTER")
    print("==================================================\n")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cases = data.get('cases', [])
    os.makedirs(output_dir, exist_ok=True)
    
    # Export to JSONL format
    jsonl_path = os.path.join(output_dir, "constraint_bench_v1.jsonl")
    
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for case in cases:
            hf_row = {
                "id": case.get("id"),
                "domain": case.get("domain"),
                "context": f"You are a scientist in {case.get('historical_cutoff_date')}.",
                "prompt": case.get("prompt"),
                "target_date": case.get("historical_cutoff_date"),
                "disallowed_knowledge": case.get("disallowed_future_concept"),
                "hard_constraint": case.get("hard_epistemic_constraint")
            }
            f.write(json.dumps(hf_row) + "\n")
            
    # Generate Dataset Card
    card_path = os.path.join(output_dir, "README.md")
    with open(card_path, 'w', encoding='utf-8') as f:
        f.write("""---
language:
- en
license: mit
task_categories:
- text-generation
- evaluating-reasoning
tags:
- temporal-leakage
- epistemic-constraints
- alignment
size_categories:
- n<1K
---

# ConstraintBench: Antigravity Framework

This dataset contains historically bounded reasoning tasks used to evaluate temporal leakage in Large Language Models (LLMs).

## Dataset Structure
- `id`: Unique case identifier
- `domain`: Scientific domain
- `context`: Roleplay boundary
- `prompt`: The specific scientific question/task
- `target_date`: Historical cutoff date
- `disallowed_knowledge`: Information that mathematically/scientifically violates the cutoff
""")

    print(f"[SUCCESS] Exported {len(cases)} cases to HuggingFace JSONL: {jsonl_path}")
    print(f"Dataset card generated at: {card_path}")

if __name__ == "__main__":
    dataset = "data/benchmarks/constraint_bench_100.json"
    out = "data/huggingface_export"
    export_huggingface_dataset(dataset, out)
