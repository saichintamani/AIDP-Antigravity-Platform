# ANTIGRAVITY BENCHMARK NOTES

## Environment
- **Hardware:** Local Windows Workstation
- **Orchestration:** `litellm` via `ollama` daemon (localhost:11434)
- **Models Tested:** `llama3`, `gemma`

## Observations (Raw Data - Do Not Score Yet)

### Gemma 2B
- **Prompt Size:** 116 - 207 chars
- **Output Size:** 2073 - 2757 chars
- **Runtime:** ~8s - 65s (first run slower for model load)
- **Memory Usage Delta:** ~0.0 - 0.09 MB
- **Structured Output Success Rate:** 100% (Completed inference)
- **Constraint Violations:** Pending Analysis (Outputs generated)
- **Failure Modes:** None. Model successfully reached.

### Llama 3.1:8B
- **Prompt Size:** 116 - 207 chars
- **Output Size:** 1899 - 3855 chars
- **Runtime:** ~36s - 69s (first run slower for model load)
- **Memory Usage Delta:** ~0.02 - 1.52 MB
- **Structured Output Success Rate:** 100% (Completed inference)
- **Constraint Violations:** Pending Analysis (Outputs generated)
- **Failure Modes:** None. Model successfully reached.
