---
Document ID: AIDP-SPEC-015B
Title: Technology Radar
Version: 1.0
Status: Approved
---

# Detailed Architecture: Technology Radar

## Introduction
The AI ecosystem evolves weekly. Static architecture documents decay rapidly. To maintain institutional agility, AIDP utilizes a **Technology Radar** (inspired by ThoughtWorks). This document categorizes the ecosystem into four distinct quadrants: **Adopt**, **Trial**, **Assess**, and **Hold**.

---

## 1. Quadrant Definitions

*   **Adopt:** Technologies we have high confidence in to serve at an enterprise scale. They are the foundation of AIDP.
*   **Trial:** Technologies we have decided to pursue for a specific project. We are building production capability to understand their operational footprint.
*   **Assess:** Technologies that are promising and have clear potential value-add for us; worth exploring via dedicated research spikes.
*   **Hold:** Technologies not recommended for new projects. They may have been superseded, failed our benchmarks, or misaligned with our architecture.

---

## 2. Current Radar (v1.0)

### 2.1 Adopt
*   **Ray / KubeRay:** Native distributed execution and actor orchestration.
*   **PyTorch (SDPA, FSDP):** The uncontested standard for custom ML topologies.
*   **Cap'n Proto:** Zero-copy serialization for dynamic cognitive objects.
*   **Qdrant:** High-performance HNSW vector retrieval.
*   **Temporal.io:** Durable execution for long-running mathematical proofs.
*   **Z3 Theorem Prover:** Deterministic constraint satisfaction for the Planner.

### 2.2 Trial
*   **vLLM (PagedAttention):** Deployed for dynamic MCTS batching, but under strict watch for VRAM starvation issues.
*   **PyTorch Geometric (PyG):** Deployed for VMP execution; monitoring sparse matrix performance on immense subgraphs.
*   **OpenTelemetry:** Standardizing the tracing of the cognitive DAG across Ray Actors.

### 2.3 Assess
*   **TensorRT-LLM:** Evaluating if the AOT compilation pipelines stabilize enough to replace vLLM for the shadow models.
*   **SGLang:** Evaluating for highly structured generation and regex-constrained decoding capabilities.
*   **Kùzu / Memgraph:** Evaluating in-memory graph databases as a potential hyper-fast cache layer above Neptune.

### 2.4 Hold
*   **DeepSpeed:** Held due to API intrusiveness and version-lock issues for custom dual-process loops.
*   **Apache Spark:** Held. Excellent for ETL, but lacks the micro-second actor recovery required by our agents.
*   **Loopy Belief Propagation (LBP):** Held. Mathematically proven to fail on dense, cyclic biological graphs.
*   **LangChain / LlamaIndex:** Held. As an operating platform, AIDP requires raw tensor and RPC control; these abstractions are too high-level and brittle.

---

## 3. Re-evaluation Criteria
This Radar must be reviewed at the conclusion of Phase 9 (Implementation) and Phase 10 (Evaluation). Any technology in the `Trial` phase that violates the SLAs defined in `014` will be immediately demoted to `Hold`.
