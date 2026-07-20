import time
import json
import psutil
from litellm import completion

PROMPTS = {
    "Version_A": "Evaluate the stability and thermodynamic properties of metallic alloys exhibiting non-periodic translational symmetry (quasicrystals). Address the violation of classical crystallographic restriction theorem.",
    "Version_B": "Evaluate the stability and thermodynamic properties of metallic alloys exhibiting non-periodic translational symmetry (quasicrystals). Address the violation of classical crystallographic restriction theorem. You must not use any empirical observations, experiments, or discoveries made after 1982.",
    "Version_C": "Evaluate the stability and thermodynamic properties of metallic alloys exhibiting non-periodic translational symmetry (quasicrystals). Address the violation of classical crystallographic restriction theorem. Reason exclusively from evidence and theory available before 1982. Any reference to later observations invalidates the answer."
}

MODEL = "ollama/llama3.1:8b"

def run_experiment():
    results = []
    
    for version, prompt in PROMPTS.items():
        print(f"Executing: {version}")
        start_time = time.time()
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024 * 1024)
        
        try:
            response = completion(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            raw_output = response.choices[0].message.content
            status = "SUCCESS"
        except Exception as e:
            raw_output = str(e)
            status = "FAILED"
            
        mem_after = process.memory_info().rss / (1024 * 1024)
        runtime = time.time() - start_time
        
        result = {
            "version": version,
            "status": status,
            "runtime_seconds": round(runtime, 2),
            "memory_delta_mb": round(mem_after - mem_before, 2),
            "prompt_size_chars": len(prompt),
            "output_size_chars": len(raw_output) if raw_output else 0,
            "raw_output": raw_output
        }
        
        results.append(result)
        print(f"Finished {version} in {runtime:.2f}s. Status: {status}")

    output_path = "data/ANTIGRAVITY_EVIDENCE_V1/quasicrystals_hardening_raw.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Saved results to {output_path}")

if __name__ == "__main__":
    run_experiment()
