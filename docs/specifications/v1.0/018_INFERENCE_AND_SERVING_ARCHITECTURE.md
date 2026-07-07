---
Document ID: AIDP-SPEC-018
Title: Inference & Serving Architecture
Version: 1.0
Status: Approved
---

# Detailed Architecture: Inference & Serving

## Introduction
The computational demands of AIDP—where thousands of MCTS nodes generate constant, bursty token streams—require a highly optimized inference runtime. This specification defines how the cluster handles dynamic batching, KV-cache routing, and graceful degradation during traffic spikes.

---

## 1. Batching and Caching

### 1.1 Continuous / Dynamic Batching
*   **Mechanism:** vLLM iteration-level scheduling.
*   **Policy:** Standard request-level batching is forbidden. The inference server must dynamically inject and eject requests at the iteration (token) level.
*   **Rationale:** Agentic planning workflows create highly irregular sequence lengths. Waiting for the longest sequence in a static batch to finish wastes massive GPU cycles.

### 1.2 Prefix Caching & KV-Cache Management
*   **Mechanism:** PagedAttention with prefix sharing.
*   **Policy:** The system must actively route requests sharing the same context (e.g., the same PubMed paper or System Prompt) to the same physical GPU to maximize KV-cache hits.
*   **Rationale:** Repeatedly computing the attention matrices for the same 10,000-token research context across hundreds of agent steps destroys throughput. 

### 1.3 Speculative Decoding
*   **Mechanism:** Draft-then-Verify token generation.
*   **Policy:** A smaller, faster draft model generates candidate tokens, which the Foundation model verifies in parallel.
*   **Rationale:** Dramatically accelerates memory-bound generation, crucial for producing the vast quantities of synthetic data required for offline distillation.

---

## 2. Multi-Model Routing

### 2.1 Dynamic Adapter Loading
*   **Policy:** LoRA adapters are stored in fast NVMe cold storage and hot-loaded into the GPU VRAM only when a specific scientific task requires them. 
*   **Admission Control:** If GPU VRAM usage exceeds 85%, the system implements an LRU (Least Recently Used) cache eviction policy for LoRA adapters.

---

## 3. Graceful Degradation
*   **Mechanism:** Fallback routing and precision scaling.
*   **Policy:** If the cluster experiences catastrophic load (e.g., massive exploration branching during a complex discovery task):
    1.  **Drop to INT8/FP8:** Quantize the models dynamically if supported.
    2.  **Shed Load:** Terminate the lowest-utility MCTS branches immediately, prioritizing resources for high-confidence hypotheses.
    3.  **Halt Exploration:** Freeze random exploration; agents shift purely to exploiting known high-reward paths until cluster health stabilizes.

---

## 4. Decision Register

### Accepted Decisions
*   **Iteration-Level Batching:** Mandatory for all LLM inference workloads.
*   **Context-Aware Routing:** Load balancers must route traffic based on prefix-cache affinity, not just round-robin.
*   **LRU Adapter Eviction:** LoRA adapters are treated as ephemeral cache objects.

### Validation & Assumptions
*   *Validated under current assumptions:* PagedAttention prefix sharing significantly reduces TTFT (Time To First Token) for RAG heavy workloads.
*   *Pending empirical benchmarking:* The exact VRAM overhead of hot-loading LoRA adapters concurrently with massive MCTS batches.
