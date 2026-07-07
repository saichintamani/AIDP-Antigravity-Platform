---
Document ID: AIDP-SPEC-016
Title: Foundation Model Architecture
Version: 1.0
Status: Approved
---

# Detailed Architecture: Foundation Model Roles

## Introduction
A mature AI platform does not treat all models equally. Treating a massive causal reasoning model the same as a hyper-fast planning network leads to catastrophic architectural bottlenecks. This specification defines the exact **Roles, Boundaries, and Adaptation Strategies** for every model within the AIDP ecosystem.

---

## 1. Model Topologies and Roles

### 1.1 Foundation Models (The Causal Core)
*   **Role:** Broad epistemic reasoning, causal hypothesis generation, and zero-shot synthesis across scientific domains.
*   **State:** **Frozen.**
*   **Adaptation:** Strictly Prompt Engineering, In-Context Learning (RAG/PPR context), and Tool-use fine-tuning.
*   **Example Equivalent:** LLaMA-3 70B, GPT-4 class models.
*   **Rationale:** The computational cost of full-parameter fine-tuning on a 70B model destroys agility. The foundation model remains frozen to ensure generalized world-knowledge is preserved, while domain-specificity is injected at inference time via the Knowledge Substrate (`008`).

### 1.2 Specialist Models (Domain Adapters)
*   **Role:** High-accuracy prediction on narrow scientific tasks (e.g., molecular property prediction, binding affinity, genomic sequence alignment).
*   **State:** **Fine-Tuned.**
*   **Adaptation:** Low-Rank Adaptation (LoRA) or QLoRA. 
*   **Lifecycle:** Specialist models are attached to the Foundation Model as dynamic adapters. They support **Continual Learning** as new scientific datasets are ingested.
*   **Rationale:** A single Foundation Model cannot natively predict precise binding affinities without catastrophic forgetting. LoRA adapters allow the agent to swap domain expertise in milliseconds.

### 1.3 Distilled Models (The Planning Engine)
*   **Role:** Sub-millisecond evaluation of states and actions during Monte Carlo Tree Search (MCTS) rollouts.
*   **State:** **Continuously Distilled.**
*   **Architecture:** Non-autoregressive Continuous Actor-Critic MLPs (Multi-Layer Perceptrons).
*   **Lifecycle:** The Foundation Model's high-latency reasoning trace is asynchronously distilled into these fast, reactive networks via Offline Reinforcement Learning (DPO/PPO).
*   **Rationale:** As proven in `014A`, autoregressive LLMs violate the 100ms planning SLA. The Distilled Models act as the "Type 1" fast-thinking system, operating independently of the "Type 2" Foundation Model.

### 1.4 Symbolic Components (The Verifiers)
*   **Role:** Deterministic constraint satisfaction and logical verification.
*   **State:** **Deterministic / Non-Learned.**
*   **Technology:** Z3 Theorem Prover, SymPy.
*   **Rationale:** Neural networks hallucinate. Symbolic components are used by the Critic Agent to formally verify hypotheses (e.g., verifying mass conservation in a proposed chemical reaction) before the hypothesis is admitted to the Subjective Logic engine.

---

## 2. Adaptation and Plasticity

| Model Role | Plasticity | Training Method | Deployment Topology |
| :--- | :--- | :--- | :--- |
| **Foundation** | Frozen | None | PyTorch FSDP (Sharded across cluster) |
| **Specialist** | High | LoRA / QLoRA | Attached dynamically to Foundation instances |
| **Distilled** | High | Offline RL Distillation | Single-Node Tensor Parallel (Zero network latency) |
| **Symbolic** | None | N/A | Embedded directly in Ray Actors |

---

## 3. Decision Register

### Accepted Decisions
*   **Frozen Foundation Core:** The primary 70B causal model will not undergo full-parameter fine-tuning to preserve general reasoning and avoid catastrophic forgetting.
*   **Dynamic LoRA Swapping:** Domain-specific knowledge (e.g., protein folding vs. pathway analysis) is handled strictly through dynamically loaded LoRA adapters.
*   **Asynchronous Distillation:** The MCTS Actor-Critic networks are decoupled from the Foundation Model and trained asynchronously via offline traces.

### Validation & Assumptions
*   *Validated under current assumptions:* Dynamic LoRA loading within vLLM introduces negligible latency ($< 10$ms). 
*   *Pending empirical benchmarking:* The offline RL distillation pipeline's ability to maintain high alignment with the Foundation Model's reasoning over hundreds of thousands of state trajectories.
