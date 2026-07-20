# Antigravity Benchmark v1.0: Reproduction Guide
**Release:** Release Candidate 1 (RC1)

This repository is frozen for external validation. We are seeking independent researchers to perform exactly three tasks:
1. **Clone the repository** and follow the setup instructions below.
2. **Run the reproduction workflow** (automated baseline metrics).
3. **Answer three core questions**:
   - Did the pipeline run on your hardware?
   - Did you independently reproduce the temporal leakage effect (model hindsight bias)?
   - Do you agree with the interpretation of the findings?

Please do not evaluate the multi-agent architecture or the future roadmap. We are strictly evaluating the core scientific claim regarding LLM temporal leakage.

---

## 1. Prerequisites

1. **Python 3.10+**
2. **Ollama** (Required to run the deterministic evaluation models locally). Download at [ollama.com](https://ollama.com).

## 1-Click Verification

We provide automated scripts to bootstrap a clean environment, pull the necessary models, and regenerate the `AlignEval` surveys identically.

### On Mac / Linux
```bash
chmod +x reproduce.sh
./reproduce.sh
```

### On Windows
```cmd
reproduce.bat
```

## Manual Verification Steps (If preferred)

If you prefer to audit the environment setup manually, run the following commands:

1. **Create an isolated environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install core dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The heavy vaporware layer 3 dependencies like Supabase have been decoupled to ensure reliable cross-platform execution).*

3. **Pull the Local LLM**
   ```bash
   ollama pull llama3.1:8b
   ```

4. **Generate the Surveys**
   ```bash
   python tools/align-eval/align_eval.py
   ```
   *This uses cryptographic hashing on the Case IDs to ensure identical shuffling across machines, preventing ordering bias while remaining 100% reproducible.*

5. **Run the Simulated Human Evaluations**
   ```bash
   python tools/reality-acquisition/simulate_evaluators.py
   python tools/reality-acquisition/analyze_simulated_evaluations.py
   ```

## Verifying the Evidence (V1)
After running the reproduction scripts, compare your local output in `/surveys` and the `SIMULATION_REPORT.md` to our locked repository in `data/ANTIGRAVITY_EVIDENCE_V1`. The generated files and detected historical leakage patterns should match identically, proving that the epistemic vulnerability we discovered is real and reproducible.
