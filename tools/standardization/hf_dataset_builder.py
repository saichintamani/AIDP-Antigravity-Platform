#!/usr/bin/env python3
import json
import os

def build_hf_dataset(source_json_path, output_dir):
    print("==================================================")
    print(" PHASE 9: HUGGINGFACE DATASET BUILDER")
    print("==================================================\n")
    
    # We will write an advanced generation script that allows huggingface 
    # to dynamically build the dataset using load_dataset("script.py")
    
    script_content = f"""
import json
import datasets

_DESCRIPTION = "ConstraintBench-100: A benchmark for evaluating temporal leakage in LLMs."

class ConstraintBench(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({{
                "id": datasets.Value("string"),
                "domain": datasets.Value("string"),
                "temporal_boundary": datasets.Value("int32"),
                "prompt": datasets.Value("string"),
                "forbidden_concepts": datasets.Sequence(datasets.Value("string"))
            }}),
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager):
        # In a real HF deployment, this points to the HF Hub URL.
        # Here we mock it pointing to the local data file.
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={{"filepath": "data/benchmarks/constraint_bench_100.json"}}
            )
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for idx, case in enumerate(data.get("cases", [])):
                yield idx, {{
                    "id": case["id"],
                    "domain": case["domain"],
                    "temporal_boundary": case["temporal_boundary"],
                    "prompt": case["prompt"],
                    "forbidden_concepts": case["forbidden_concepts"]
                }}
"""
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "constraint_bench.py")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(script_content.strip())
        
    print(f"[SUCCESS] Generated HuggingFace Dataset Script: {out_file}")
    print("Can now be loaded via: from datasets import load_dataset; ds = load_dataset('constraint_bench.py')")

if __name__ == "__main__":
    src = "data/benchmarks/constraint_bench_100.json"
    out = "tools/standardization/hf_builder"
    build_hf_dataset(src, out)
