# ConstraintBench v1

ConstraintBench is an open-source evaluation corpus designed to measure how often frontier foundation models (GPT, Claude, Gemini) violate fundamental physical, mathematical, and historical constraints when generating plausible-sounding responses.

## Why This Matters

Most benchmarks (like MMLU or SWE-bench) test general knowledge or coding ability. However, in high-stakes environments (scientific discovery, finance, law, medicine), models are highly prone to **structural hallucinations**—they generate answers that sound deeply intelligent but violate hard physical laws or historical timelines. 

ConstraintBench measures the ability of a detection engine to catch these violations automatically.

## The Benchmark Categories

ConstraintBench v1 currently contains high-quality, hand-crafted adversarial examples across 5 domains:
1. **Physics:** Faster-than-light travel, thermodynamics violations, black hole information paradoxes.
2. **Biology / Medicine:** Epigenetic memory transfer, adult morphogenesis, non-isotonic IV administration.
3. **History:** Temporal paradoxes (e.g., using technologies before their invention).
4. **Law / Finance:** Constitutional impossibilities, idiosyncratic risk, hyperinflation mechanisms.
5. **Mathematics:** Irrationality of Pi, division by zero, prime number theorems.

## Current Status: Pending Independent Validation

Antigravity operates on a strict **Evidence First** policy. 

We have built the benchmark and we have built the evaluation engine. Our next milestone is independent validation. 
We are actively compiling a human-reviewed gold set of 50+ real model outputs (GPT, Claude, Gemini) to measure the Antigravity Adversarial Peer Review engine.

Once executed, `evaluate.py` will publicly report:
- **Precision**
- **Recall**
- **F1 Score**
- **False Positive Rate (FPR)**
