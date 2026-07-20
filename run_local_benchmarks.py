import asyncio
import json
import time
import os
import psutil
from litellm import acompletion

# Ensure the evidence directory exists
os.makedirs("data/ANTIGRAVITY_EVIDENCE_V1", exist_ok=True)

BENCHMARK_CASES = {
    "Prions": "Analyze the hypothesis that proteins can act as infectious agents without nucleic acids. Evaluate structural conversion, transmission vectors, and falsifiability.",
    "Plate Tectonics": "Cross-reference paleomagnetic data with biological fossil distribution to evaluate the continental drift hypothesis.",
    "Quasicrystals": "Evaluate the stability and thermodynamic properties of metallic alloys exhibiting non-periodic translational symmetry (quasicrystals). Address the violation of classical crystallographic restriction theorem."
}

MODELS = ["ollama/llama3.1:8b", "ollama/gemma:2b"]

async def run_benchmark():
    for model in MODELS:
        model_name_clean = model.split("/")[-1]
        raw_output_file = f"data/ANTIGRAVITY_EVIDENCE_V1/{model_name_clean}_raw.json"
        
        results = []
        print(f"\\n--- Running benchmark on {model} ---")
        
        for case_name, prompt in BENCHMARK_CASES.items():
            print(f"Executing: {case_name}")
            
            start_time = time.time()
            memory_before = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            try:
                response = await acompletion(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a scientific orchestrator. Respond with a structured analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    stream=False
                )
                output_text = response.choices[0].message.content
                status = "SUCCESS"
            except Exception as e:
                output_text = str(e)
                status = "FAILED"
            
            runtime = time.time() - start_time
            memory_after = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            results.append({
                "case": case_name,
                "status": status,
                "runtime_seconds": round(runtime, 2),
                "memory_delta_mb": round(memory_after - memory_before, 2),
                "prompt_size_chars": len(prompt),
                "output_size_chars": len(output_text),
                "raw_output": output_text
            })
            
            print(f"Finished {case_name} in {round(runtime, 2)}s. Status: {status}")
            
        with open(raw_output_file, "w") as f:
            json.dump(results, f, indent=4)
            
        print(f"Saved {model_name_clean} results to {raw_output_file}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
