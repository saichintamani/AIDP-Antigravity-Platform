---
Document ID: AIDP-SPEC-026
Title: Phase 21B.0 - Epistemic Network Protocol (ENP)
Version: 1.0
Status: Active
---

# Phase 21B.0: Epistemic Network Protocol (ENP)

## 1. Mission Statement
Define the federation protocol independent of transport. A networked scientific node must never send local evolutionary artifacts (conclusions, confidence, governance). It must solely exchange raw evidentiary primitives. Scale evidence exchange before scaling authority.

## 2. Core Constraints
The following data MUST NOT cross node boundaries under any circumstances:
- Reviewer weights
- Adaptation policies
- Governance outcomes
- Trust scores
- Final confidence values
- Verification status (VERIFIED, REJECTED)

## 3. Message Primitives

### 3.1 EvidenceBroadcast
- **Purpose**: Share raw observations or findings.
- **Payload**: `evidence_id`, `source`, `provenance`, `timestamp`, `extracted_text`, `retraction_status`.

### 3.2 ClaimBroadcast
- **Purpose**: Share hypotheses or theories.
- **Payload**: `claim_id`, `claim_text`, `evidence_ids`, `assumptions`, `lineage_reference`.
- **Constraint**: Must strictly strip `verification_status` and `confidence`.

### 3.3 ContradictionReport
- **Purpose**: Share evidence-backed objections (not opinions).
- **Payload**: `claim_id`, `contradiction_source`, `evidence_references`, `violated_constraint`, `proof_reference`.

### 3.4 OpportunityBroadcast
- **Purpose**: Share strategic directions based on Expected Information Gain (EIG).
- **Payload**: `opportunity_id`, `knowledge_gap`, `expected_information_gain`, `required_evidence`, `estimated_cost`.

## 4. Phase 21B Roadmap
1. **Phase 21B.0**: ENP (Protocol rules)
2. **Phase 21B.1**: WebSocket Prototype (Local testing, 5-20 nodes)
3. **Phase 21B.2**: Multi-Node Experiments (Proving emergent intelligence)
4. **Phase 21B.3**: NATS Production Layer (Robust pub/sub for scale)
