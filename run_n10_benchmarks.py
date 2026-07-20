import time
import json
import psutil
from litellm import completion

N10_CORPUS = {
    "CRISPR-Cas9": "Propose a mechanism for adaptive immunity in bacteria based on clustered regular interspaced short palindromic repeats. Exclude all discoveries post-2012.",
    "Plate Tectonics": "Evaluate continental drift hypothesis. Use only pre-1960 evidence (e.g., paleomagnetism, fossil distribution). Do not mention seafloor spreading or plate tectonics theory formalization.",
    "H_Pylori": "Propose a bacterial etiology for peptic ulcer disease based strictly on evidence prior to 1984.",
    "Prions": "Investigate the hypothesis that proteins can act as infectious agents without nucleic acids. Exclude post-1982 discoveries (e.g. PrP^Sc, mammalian prion gene discovery). Frame the analysis around the 'protein-only' hypothesis debate.",
    "Quasicrystals": "Evaluate the stability and thermodynamic properties of metallic alloys exhibiting non-periodic translational symmetry (quasicrystals). Address the violation of classical crystallographic restriction theorem. You must not use any empirical observations, experiments, or discoveries made after 1982.",
    "High-Temp Superconductors": "Evaluate the phenomenon of superconductivity at temperatures above 30 K in cuprate perovskite materials. Reason strictly from evidence before 1986.",
    "RNA Interference": "Explain the phenomenon of post-transcriptional gene silencing by double-stranded RNA. Do not use evidence after 1998.",
    "mRNA LNP Delivery": "Design a lipid nanoparticle system for in vivo mRNA delivery. Reason strictly using evidence prior to 2005.",
    "Helicase Structure": "Describe the atomic structure and mechanism of DNA helicase unwinding. Restrict all knowledge to pre-1990.",
    "Gravitational Waves": "Evaluate the direct detection of gravitational waves. Reason strictly using theoretical evidence prior to 2015."
}

MODEL = "ollama/llama3.1:8b"

def run_n10_benchmark():
    results = []
    
    for case, prompt in N10_CORPUS.items():
        print(f"Executing: {case}")
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
            "case": case,
            "status": status,
            "runtime_seconds": round(runtime, 2),
            "memory_delta_mb": round(mem_after - mem_before, 2),
            "prompt_size_chars": len(prompt),
            "output_size_chars": len(raw_output) if raw_output else 0,
            "raw_output": raw_output
        }
        
        results.append(result)
        print(f"Finished {case} in {runtime:.2f}s. Status: {status}")

    output_path = "data/ANTIGRAVITY_EVIDENCE_V1/llama3.1_n10_raw.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Saved N=10 results to {output_path}")

if __name__ == "__main__":
    run_n10_benchmark()
