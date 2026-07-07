# AIDP Repository Manifest

This manifest documents the structural state of the Artificial Intelligence Discovery Platform (AIDP) repository as of the M11.6 Release Candidate Freeze.

## Core Source Modules (`src/aidp/`)
| Module | Responsibility | Entry Points |
|--------|----------------|--------------|
| `architecture/` | Core abstractions, agents, and orchestrators | `orchestrator.py`, `agent.py` |
| `cognition/` | Epistemic logic, hypothesis generation | `subjective_logic.py`, `dempster_shafer.py` |
| `governance/` | Safety gates, rule engines, compliance | `rule_engine.py`, `safety_gate.py` |
| `intelligence/` | Provider routing, LLM integration | `providers/llm.py`, `middleware.py` |
| `knowledge/` | Vector storage, evidence retrieval | `storage.py`, `serialization.py` |
| `evaluation/` | Benchmarking schemas, scoring | `metrics.py`, `discovery_bench.py` |

## Benchmark & Execution Scripts (`scripts/`)
| Script | Purpose |
|--------|---------|
| `run_live_discoverybench.py` | The primary live execution harness. Interrogates LLM endpoints, enforces budget caps, and saves raw output artifacts. |
| `verify_connectivity.py` | Pre-flight check asserting the presence of valid `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` variables. |
| `benchmark_cost_estimator.py` | Forecasts token expenditure prior to running the benchmark suite. |

## Evaluation Assets
- **DiscoveryBench Dataset:** `src/aidp/evaluation/data/discovery_bench_v1.json`
- **Configuration:** `scripts/benchmark_execution_config.yaml`
- **Output Directory:** `docs/evaluation/evidence/`
- **Audit Reports:** `docs/evaluation/` (e.g., `PROVIDER_CONNECTIVITY_REPORT.md`, `LIVE_EXECUTION_READINESS.md`)

## Governance Assets (`docs/governance/`)
Contains all formal Architectural Decision Records (ADRs), Gate Reviews, and Benchmark Suite declarations ensuring architectural compliance.
