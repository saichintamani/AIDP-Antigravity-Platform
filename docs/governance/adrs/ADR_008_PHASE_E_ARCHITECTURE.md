# ADR-008: Self-Improving Scientific Intelligence (Phase E)

## Status
Proposed

## Context
AIDP currently possesses robust orchestration (Phase D), resource governance (Phase C), and cognitive reasoning (Phase B). The original plan for Phase E was to train or fine-tune a "Scientific Foundation Model" (RLHF/RLAIF). However, training foundation models is resource-intensive and does not inherently differentiate AIDP from massive AI labs. Instead, the true differentiator for AIDP is a system that learns *at the architectural and prompting level*—a self-improving meta-system.

## Decision
We will redefine Phase E as **Self-Improving Scientific Intelligence**. We will pivot from weight-level fine-tuning to system-level continuous learning.

### 1. Scientific Experience Replay (E1) & Discovery Memory (E6)
- The system will log successful hypotheses, failed experiments, and debate outcomes.
- We will build a `DiscoveryMemory` that allows the system to query past campaigns to prevent repeating failed logic and to surface reasoning patterns that previously yielded high Expected Information Gain (EIG).

### 2. Autonomous Prompt Evolution (E2) & Policy Learning (E3)
- Prompts will no longer be hard-coded strings. They will become versioned assets.
- The system will A/B test prompt variations and routing policies, automatically promoting variants that yield higher `DiscoveryValue` scores and rolling back regressions.

### 3. Scientific Curriculum (E7) & Autonomous Research Academy (E10)
- Agents will have a `ScientificSkillGraph` (E4). If the system detects a weakness (e.g., poor statistical critique), it generates internal curriculum exercises for that agent class.
- New agents will undergo simulated campaigns and peer-review certification before touching the live `IntelligentScheduler`.

### 4. Discovery Simulator (E9) & Benchmarking (E5)
- We will build a simulator that ingests historical literature (e.g., 2020-2022) while hiding future papers, asking AIDP to predict discoveries.
- This creates an automated benchmark to track system novelty, correctness, and reproducibility over time.

## Consequences
- **Positive**: AIDP transforms into an autonomous entity that improves without human engineering or expensive GPU cycles. It establishes a strong differentiation as a "learning laboratory."
- **Negative**: The complexity of managing versioned prompts, A/B testing logic, and skill graphs is non-trivial and will require careful database schema design for the `DiscoveryMemory`.
