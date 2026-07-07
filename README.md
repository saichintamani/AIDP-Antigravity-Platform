# AIDP (Artificial Intelligence Discovery Platform) Version 1.0

AIDP is an Operating System for Autonomous Scientific Discovery. It moves beyond static LLM prompts to provide a fully functioning, autonomous laboratory architecture.

## Core Features
1. **Cognitive Core**: Provenance tracking and hierarchical memory.
2. **Predictive Scientific Reasoning Engine (PSRE)**: Evaluates, debates, and simulates experimental designs using Subjective Logic before execution.
3. **ResearchOps**: Autonomous budget governance and token tracking.
4. **Self-Improving Meta-Learning**: Autonomous prompt evolution and experience replay.
5. **Scientific Evaluation Framework**: Generates 12-dimensional report cards for every campaign.

## Quickstart
Launch the laboratory dashboard:
```bash
uv run streamlit run src/aidp/platform/dashboard/app.py
```
Launch the API Gateway:
```bash
uv run python src/aidp/platform/api/main.py
```

## Demonstrations
View the end-to-end capabilities by running the V1.0 live demo:
```bash
uv run python scripts/demonstrations/live_demo.py
```

## Validation & Benchmarks
AIDP V1.0 is validated against historical breakthroughs (masking future literature). See `data/benchmarks/` for DiscoveryBench.
