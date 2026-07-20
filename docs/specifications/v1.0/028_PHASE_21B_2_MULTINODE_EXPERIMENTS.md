---
Document ID: AIDP-SPEC-028
Title: Phase 21B.2 - Multi-Node Collective Experiments
Version: 1.0
Status: Active
---

# Phase 21B.2: Multi-Node Collective Experiments

## 1. Mission Statement
Demonstrate emergent intelligence in the AIDP collective by solving the "Fragmented Knowledge" problem across a physical network of independent nodes, proving that federation accelerates discovery beyond the capacity of isolated systems.

## 2. The Fragmented Knowledge Benchmark
The hallmark of a high-functioning collective intelligence is the ability to synthesize disparate pieces of evidence held by different actors into a single verified breakthrough, without any central orchestration.

**Scenario**:
- A scientific claim requires three independent pieces of evidence (X, Y, and Z) to be formally verified.
- The network consists of 5 independent nodes (A, B, C, D, E) connected via a peer-to-peer WebSocket mesh using the Epistemic Network Protocol (ENP).
- Node A possesses the Hypothesis (the Claim) and Evidence X.
- Node B possesses Evidence Y.
- Node C possesses Evidence Z.

**Initial State**: No single node can verify the claim. Isolated science fails.
**Expected Emergent State**: As nodes broadcast their evidence primitives, the mesh synchronizes the evidence pools. Ultimately, all nodes independently evaluate the claim against their newly complete evidence pools and arrive at a `VERIFIED` status.

## 3. Epistemic Constraints
- Nodes MUST NOT exchange verification statuses. 
- Nodes MUST NOT exchange confidence scores.
- Nodes MUST independently compute the final `VerificationStatus` using their local verifier functions.

## 4. Next Steps
Successfully passing this integration test fulfills the theoretical prerequisites of the Federation Architecture. The final step is Phase 21B.3: NATS Production Layer, to scale this architecture to thousands of nodes using enterprise-grade messaging.
