# Repository-Wide Capability Audit

This audit evaluates every major subsystem within the Artificial Intelligence Discovery Platform (AIDP) to identify standalone product value, explicitly measuring their independence from AIDP's core hypothesis (i.e., whether they remain valuable even if the generative discovery engine completely fails).

---

## 1. Product Candidates
*High commercial value, highly independent of AIDP's generative success, solves an acute enterprise or research pain point today.*

### A. AlignEval (Blinded Alignment Workflow)
- **Purpose:** Cryptographically seeds and generates blinded evaluation surveys for human domain experts.
- **Pain Point:** Gathering unbiased expert consensus for RLHF or peer-review is operationally tedious and highly susceptible to candidate ordering bias.
- **Value if AIDP fails:** Retains 100% of its value. Researchers will always need to evaluate models and humans against each other.
- **Scores:** Commercial (7/10) | Defensibility (4/10) | Time to MVP (1/10 - *Already Built*) | Independence (10/10)
- **Verdict:** Immediate Go-to-Market Product.

### B. Adversarial Peer Review (Constraint Validation Engine)
- **Purpose:** Forces LLM outputs to adhere strictly to mathematical, physical, and historical constraints extracted from literature.
- **Pain Point:** Enterprise LLMs hallucinate physics, math, and logic, rendering them useless for high-stakes scientific or financial applications.
- **Value if AIDP fails:** Immense. If generative AI cannot discover new science, it still needs strict guardrails for standard operations. A standalone "Physics/Math Linter for LLMs" is highly valuable.
- **Scores:** Commercial (9/10) | Defensibility (8/10) | Time to MVP (4/10) | Independence (10/10)
- **Verdict:** Primary Enterprise Product Candidate.

### C. Epistemic Engine (Decision Provenance Ledger)
- **Purpose:** Immutably traces the exact chain of logic, raw data, prompts, and context that led to an AI decision.
- **Pain Point:** Enterprise AI is a black box. In regulated industries (Pharma, Finance, Law), knowing *why* an AI made a decision 6 months ago is a legal requirement.
- **Value if AIDP fails:** Immense. As agentic swarms become common, debugging and auditing their logic chains will be a massive industry.
- **Scores:** Commercial (9/10) | Defensibility (9/10) | Time to MVP (6/10) | Independence (10/10)
- **Verdict:** Long-term Enterprise Product Candidate.

---

## 2. Infrastructure Candidates
*Valuable tools for internal use or open-source research communities, but harder to monetize as standalone commercial products.*

### A. Historical Replay Framework (Hindsight-Cutoff Benchmarking)
- **Purpose:** Tests models on historical data without letting them cheat using future knowledge (e.g., stopping the context window at 1982 for Quasicrystals).
- **Pain Point:** Current AI benchmarks (MMLU, SWE-bench) are contaminated because the models were trained on the test sets.
- **Value if AIDP fails:** High. AI evaluation labs desperately need un-gameable benchmarks.
- **Scores:** Commercial (8/10) | Defensibility (6/10) | Time to MVP (3/10) | Independence (10/10)
- **Verdict:** High-value Open Source Infrastructure.

### B. Neurosymbolic Temporal Knowledge Graph (Data Ingestion)
- **Purpose:** Parses unstructured scientific PDFs into strict ontological triples with temporal markers.
- **Pain Point:** Standard RAG (Vector Search) is terrible at connecting complex, multi-hop scientific logic over time.
- **Value if AIDP fails:** Moderate. While useful, the market is already heavily saturated with KG and RAG solutions (Neo4j, LlamaIndex).
- **Scores:** Commercial (6/10) | Defensibility (8/10) | Time to MVP (7/10) | Independence (8/10)
- **Verdict:** Internal Infrastructure.

### C. The Failure Registry
- **Purpose:** Structurally logging methodological dead-ends, experimental failures, and hallucination biases.
- **Pain Point:** Science hides negative results, leading to massive duplication of effort across labs.
- **Value if AIDP fails:** High. It thrives specifically *because* experiments fail.
- **Scores:** Commercial (3/10) | Defensibility (3/10) | Time to MVP (2/10) | Independence (10/10)
- **Verdict:** Open Science Standard / Non-profit play.

---

## 3. Research Candidates
*Highly valuable if successful, but entirely dependent on the core AIDP hypothesis being correct.*

### A. Strategic Intelligence Layer (Hypothesis Generation)
- **Purpose:** Combines disparate evidence to generate novel scientific discoveries.
- **Pain Point:** Human scientists cannot synthesize millions of cross-domain papers.
- **Value if AIDP fails:** ZERO. If the engine hallucinates or generates trivial hypotheses, it is useless.
- **Scores:** Commercial (10/10) | Defensibility (7/10) | Time to MVP (10/10) | Independence (0/10)
- **Verdict:** Core Research Gamble.

---

## 4. Dead-End Candidates
*Capabilities that were necessary to build AIDP, but are vastly outperformed by existing open-source frameworks on the market.*

### A. Evolution Governor (Prompt Meta-Learning)
- **Purpose:** AI rewrites its own system prompts based on failure analysis.
- **Verdict:** **Dead-end.** Frameworks like DSPy already do this mathematically and deterministically. Not worth extracting.

### B. Federation Engine (Multi-Agent Orchestration)
- **Purpose:** Orchestrates 20+ specialized agents passing context back and forth.
- **Verdict:** **Dead-end.** The market is flooded with orchestration frameworks (LangGraph, AutoGen, CrewAI). AIDP's custom implementation has no standalone defensibility.

### C. Evidence Dashboard
- **Purpose:** Web UI for visualizing the provenance graph.
- **Verdict:** **Dead-end.** Highly coupled to AIDP's specific architecture; possesses no standalone product value.

---

## Expected Impact Ranking (Next 90 Days)

If the goal is to maximize impact and defensibility over the next 90 days, the roadmap must prioritize the components that do not rely on generative success:

1. **[IMMEDIATE] AlignEval:** Push the CLI tool to the open-source community. It takes 0 days to MVP because it is already finished.
2. **[30 DAYS] Adversarial Peer Review (Constraint Engine):** Extract the constraint-checking logic. Market it as a "Hallucination Linter" for enterprise RAG pipelines.
3. **[60 DAYS] Historical Replay Benchmarks:** Open-source the N=10 corpus. Position it as the only mathematically un-gameable benchmark for reasoning models.
4. **[90 DAYS] Epistemic Engine (Audit Ledger):** Begin abstracting the cryptographic decision-tracking architecture so it can be plugged into standard LangChain/LangGraph pipelines to provide auditability to third-party swarms.
