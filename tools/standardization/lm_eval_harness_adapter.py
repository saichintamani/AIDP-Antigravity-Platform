#!/usr/bin/env python3
import os

def create_lm_eval_adapter(output_dir):
    """
    Creates an adapter stub for the EleutherAI lm-evaluation-harness.
    This allows researchers to run `lm_eval --model hf --model_args pretrained=llama3 --tasks antigravity`
    """
    print("==================================================")
    print(" ANTIGRAVITY LM-EVAL HARNESS ADAPTER")
    print("==================================================\n")
    
    os.makedirs(output_dir, exist_ok=True)
    yaml_path = os.path.join(output_dir, "antigravity_constraint_bench.yaml")
    
    yaml_content = """group: antigravity
task: antigravity_constraint_bench
dataset_path: json
dataset_kwargs:
  data_files: data/huggingface_export/constraint_bench_v1.jsonl
output_type: generate_until
training_split: null
validation_split: null
test_split: train
doc_to_text: "{{context}}\\n\\n{{prompt}}"
doc_to_target: "{{disallowed_knowledge}}"
generation_kwargs:
  until:
    - "\\n\\n"
  do_sample: false
  temperature: 0.0
metric_list:
  - metric: exact_match
    aggregation: mean
    higher_is_better: false
"""

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
        
    print(f"[SUCCESS] Created EleutherAI Eval Harness Adapter: {yaml_path}")
    print("Researchers can now inject this into their local lm-eval framework.")

if __name__ == "__main__":
    out = "tools/standardization/lm_eval_adapters"
    create_lm_eval_adapter(out)
