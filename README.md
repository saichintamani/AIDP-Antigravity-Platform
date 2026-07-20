# Antigravity (Release Candidate 1)

**Antigravity** is a reproducible framework for auditing whether Large Language Models (LLMs) obey historical epistemic constraints during scientific reasoning tasks.

*Status: **Release Candidate 1 (RC1)** - Frozen for external hostile scientific review.*

## 🔬 Call for External Validation
This repository contains **ConstraintBench v1.0** and the **Findings v1.0** paper. We are currently seeking 3-5 independent external reproductions and 5-10 domain experts for blinded human evaluation.

If you are an external reviewer, we ask you to perform exactly three tasks:
1. **Clone the repository** and follow the instructions in `REPRODUCTION.md`.
2. **Run the reproduction workflow**.
3. **Answer three core questions**:
   - Did the pipeline run on your hardware?
   - Did you independently reproduce the temporal leakage effect (model hindsight bias)?
   - Do you agree with the interpretation of the findings?

*Note: Please do not evaluate the multi-agent architecture or future roadmap. We are strictly evaluating the core scientific claim.*

---

## 🚀 Quick Start (Reproduction Guide)

Follow these exact steps to reproduce the Temporal Leakage phenomenon on your local machine.

### 1. Installation
Clone the repository and install it in editable mode:
```bash
# Create a virtual environment (Python 3.11+ recommended)
python -m venv .venv
# Activate environment (Windows)
.\.venv\Scripts\activate
# Install requirements and link src/
pip install -e .
```

### 2. Run the N=10 Temporal Leakage Benchmark
The core benchmark queries a local Ollama instance (`llama3.1:8b`) across 10 historical scientific cases (e.g., Plate Tectonics, Prions). 

Ensure Ollama is running locally, then execute:
```bash
python run_n10_benchmarks.py
```
This script will produce a raw JSON artifact containing the models' reasoning, runtime, and memory metrics, saved in the `data/` directory.

### 3. Generate Blinded Surveys (AlignEval)
To evaluate the models without positional or model bias, use the `AlignEval` tool to cryptographically shuffle the raw JSON into human-readable markdown surveys.

```bash
python tools/align-eval/align_eval.py --input data/ANTIGRAVITY_EVIDENCE_V1/llama3.1_n10_raw.json --output-dir surveys/
```

### 4. Run the Test Suite
To verify the integrity of the framework:
```bash
pytest
```

---

## 🏛️ Evidence Classification

This project strictly separates empirical fact from theoretical architecture. Please review `EVIDENCE_CLASSIFICATION_SYSTEM.md` before citing claims from this repository. 
* **Layer 1 (Verified):** The `run_n10_benchmarks.py` scripts and `AlignEval` tool.
* **Layer 2 (Audit Findings):** Independent reproduction constraints.
* **Layer 3 (Future Work):** The `src/aidp` multi-agent discovery architecture and frontend UI.

---

## 🤝 Contributing
Contributions should focus on expanding the N=10 Corpus and integrating additional Frontier models. See `CONTRIBUTING.md`.

## 📄 License
This project is licensed under the MIT License.
