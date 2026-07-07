---
Document ID: AIDP-SPEC-015A
Title: Architecture Validation Report
Version: 1.0
Status: Approved
---

# Architecture Validation Report 015A

## Status
Review Completed — **REVISIONS REQUIRED**

## Date
2026-07-05

## Target Document
*   `015_REFERENCE_IMPLEMENTATION_STRATEGY.md`

## Executive Summary
The Reference Implementation Strategy provides a highly mature, industrialized evaluation of the open-source ML ecosystem. Adopting vLLM, PyTorch FSDP, and PyG aligns perfectly with our computational benchmarks. However, the architecture fails to isolate workloads properly, leading to guaranteed Out-Of-Memory (OOM) crashes and severe network latency violations during planning.

---

### Review Area 1 — vLLM & PyG Memory Starvation
*   **Critique:** Section 1.1 adopts vLLM, and Section 4.1 adopts PyTorch Geometric (PyG). The Risk section acknowledges memory starvation but fails to mandate a solution. By default, vLLM's PagedAttention pre-allocates ~90% of available GPU VRAM. If a Ray Actor attempts to execute a PyG Variational Message Passing (VMP) operation on the same node, the OS will instantly throw a CUDA Out-Of-Memory (OOM) error, killing the node.
*   **Risk Level:** Critical.
*   **Recommendation:** Do not attempt to run PyG and vLLM concurrently on the same hardware. Mandate **Strict Node Pool Isolation** via KubeRay taints/tolerations. vLLM must run exclusively on inference-optimized `$p5` instances, while PyG executes on memory-optimized, CPU-heavy `$r7a` instances, communicating via the Ray object store.

### Review Area 2 — FSDP Overhead on Distilled MLPs
*   **Critique:** Section 2.1 adopts PyTorch FSDP for model sharding. However, `014` mandates that the MCTS planner uses non-autoregressive distilled MLPs to achieve sub-millisecond inference. If we apply FSDP to these MLPs, the massive network communication overhead (All-Gather operations across NVLink/EFA) will dominate the compute time, destroying the 100ms MCTS SLA.
*   **Risk Level:** High.
*   **Recommendation:** Restrict FSDP **only** to the primary 70B+ Causal Discovery models. The distilled MCTS Actor-Critic networks must remain entirely un-sharded (or strictly Tensor Parallel on a single node) to guarantee zero network latency during the MCTS rollout loop.

---

## Action Items
1.  **[REVISE]** `015` to mandate strict Kubernetes Node Pool isolation for vLLM and PyG.
2.  **[REVISE]** `015` to explicitly restrict FSDP to massive models, exempting the distilled MCTS networks.
3.  **[UPDATE]** Add these mitigations to the Decision Register.
