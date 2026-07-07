---
Document ID: AIDP-SPEC-014
Title: Computational Algorithmic Architecture
Version: 1.0
Status: Draft
---

# Detailed Architecture: Computational Algorithmic Architecture

## Introduction
Mathematics dictates *what* is correct; algorithms dictate *how* it is computed. Without defining the algorithmic layer, the transition to Machine Learning frameworks devolves into guesswork. This specification bridges the mathematical boundaries defined in `013` with concrete, executable algorithms, establishing hard latency SLAs for every subsystem.

---

## 1. Algorithmic Selections

### 1.1 Knowledge Retrieval
**Mathematical Foundation:** Vector Geometry & HNSW.
**Algorithmic Selection:** **Personalized PageRank (PPR) + HNSW**
*   *Why:* Standard vector search retrieves isolated nodes. The Agent requires the surrounding topological context. We compute Personalized PageRank (using power iteration) initialized from the HNSW retrieved nodes to instantly fetch the local "Markov Blanket" of highly relevant surrounding evidence.

### 1.2 Belief Updating & Causal Inference
**Mathematical Foundation:** Subjective Logic & Variational Inference.
**Algorithmic Selection:** **Pre-Sparsified Variational Message Passing (VMP)**
*   *Why:* Standard Loopy Belief Propagation (LBP) fails to converge on graphs with tight loops (ubiquitous in biological networks). VMP guarantees convergence for Subjective Logic updates. However, to satisfy the 150ms SLA on dense graphs, a **Graph Sparsification** step is executed prior to VMP, mathematically pruning edges with a Subjective Logic covariance weight $< 1e-3$.

### 1.3 Planning & Decision Theory
**Mathematical Foundation:** Expected Utility & Markov Decision Processes.
**Algorithmic Selection:** **Monte Carlo Tree Search (MCTS) with UCT + Distilled Actor-Critic MLPs**
*   *Why:* A* requires a fully known state space. MCTS dynamically balances exploring novel hypotheses vs. exploiting known paths. Crucially, to satisfy the 100ms SLA, the MCTS simulation rollout *cannot* use an autoregressive LLM. The LLM's world model is mathematically distilled into a non-autoregressive continuous Actor-Critic MLP, allowing millions of sub-millisecond node evaluations during the MCTS expansion step.

### 1.4 Task Graph Scheduling
**Mathematical Foundation:** Convex Optimization (Relaxed ILP).
**Algorithmic Selection:** **Adaptive Large Neighborhood Search (ALNS)**
*   *Why:* While Z3 attempts exact constraint satisfaction, its 500ms timeout requires a fallback. ALNS is a meta-heuristic that rapidly mutates the Ray Actor allocation graph to find high-throughput schedules within strict millisecond bounds when Z3 fails.

---

## 2. AI Systems Benchmark Matrix
To ensure AIDP can function as a real-time operating platform, the following algorithmic latencies are mandated. Any algorithm violating these thresholds during the CI/CD pipeline will break the build.

| Component | Algorithmic Mechanism | Hard Latency SLA Target (p95) |
| :--- | :--- | :--- |
| **Vector Search** | HNSW (Qdrant) | < 15 ms |
| **Graph Context** | Personalized PageRank | < 20 ms |
| **Memory Retrieval** | Redis KV Lookup | < 5 ms |
| **Planning Step** | MCTS Expansion | < 100 ms |
| **Belief Update** | Variational Message Passing | < 150 ms |
| **Agent Step (Local)** | Shadow Model Execution | < 300 ms |
| **Reflection** | Full Critic Backpropagation | < 500 ms |

---

## 3. Decision Register

### Accepted Decisions
*   **Distilled MLPs for MCTS:** Chosen over autoregressive LLMs for the rollout phase to ensure sub-millisecond node evaluation and compliance with the 100ms SLA.
*   **Graph Sparsification for VMP:** Chosen to protect the 150ms belief-update SLA from dense topological "hairballs."
*   **MCTS for Planning:** Chosen over A* and POMDP solvers due to its ability to handle immense, partially observable state spaces.
*   **VMP for Belief Updating:** Chosen over Belief Propagation to guarantee mathematical convergence on cyclic graphs.
*   **PPR for Context Retrieval:** Chosen over simple BFS to rank subgraph relevance mathematically.

### Rejected Alternatives
*   **Loopy Belief Propagation (LBP):** Rejected. High risk of oscillatory failure in cyclic graphs.
*   **A* Search:** Rejected. Impossible to define a strictly admissible heuristic for open-ended scientific discovery.
*   **Exact ILP Scheduling:** Rejected for real-time loops. Z3 exact solving will timeout on graphs $> 100$ nodes.

### Open Questions
*   How deeply should MCTS unroll its simulations during a single Agent tick before hitting the 100ms timeout?
*   Should the PPR damping factor be dynamic based on the Agent's Epistemic Uncertainty?

### Risks
*   **MCTS Timeout:** If the LLM policy network backing MCTS is too slow, we will violate the 100ms planning SLA.
*   **VMP Computational Overhead:** While VMP guarantees convergence, its matrix operations may exceed the 150ms SLA on dense graphs.

### Validation Plan & Success Metrics
*   **Validation:** Implement a Python micro-benchmark for VMP on a synthetic graph of 10,000 nodes to measure convergence time.
*   **Metric:** 95th percentile (p95) execution times must remain strictly under the Benchmark Matrix targets.
