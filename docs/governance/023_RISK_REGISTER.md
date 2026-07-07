# 023 Risk Register

Tracks the probability and impact of systemic risks across the platform's lifecycle.

| Risk | Impact (1-5) | Probability (1-5) | Severity | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **GPU Memory Fragmentation (vLLM / Ray)** | 5 | 4 | **20 (High)** | KubeRay node isolation (taints/tolerations); explicit memory limits for PagedAttention vs VMP; prefix-caching affinity routing. |
| **Ray Scheduler Bottlenecks** | 4 | 3 | **12 (Med)** | Decouple state from actors. Use Cap'n Proto zero-copy serialization over Plasma Object Store to prevent network saturation. |
| **Qdrant Scaling Limits** | 4 | 2 | **8 (Low)** | Graph sparsification (removing redundant transitive edges); sharding collections by semantic domain. |
| **Model Drift / Catastrophic Forgetting** | 5 | 3 | **15 (High)** | Implement strict shadow/canary rollouts; utilize KL-Divergence critics before applying LoRA adapter updates. |
| **Subjective Logic Uncertainty Explosion** | 3 | 4 | **12 (Med)** | Bound uncertainty propagation in deep traversal trees by implementing an entropy-based pruning threshold during MCTS rollouts. |
