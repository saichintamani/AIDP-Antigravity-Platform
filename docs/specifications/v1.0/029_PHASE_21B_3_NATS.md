---
Document ID: AIDP-SPEC-029
Title: Phase 21B.3 - NATS Production Layer
Version: 1.0
Status: Active
---

# Phase 21B.3: NATS Production Layer

## 1. Mission Statement
Migrate the AIDP collective from a local peer-to-peer WebSocket mesh to a highly scalable, topic-based Pub/Sub architecture using NATS. This decouples nodes from needing to know their peers and enables massive scaling.

## 2. Topic Taxonomy
The NATS broker routes messages based on the Epistemic Network Protocol (ENP). The subjects are:

- `aidp.evidence.broadcast`
- `aidp.claim.broadcast`
- `aidp.contradiction.report`
- `aidp.opportunity.broadcast`

Nodes subscribe to these subjects. When they have new knowledge to share, they publish to these subjects.

## 3. Architecture
- **NatsFederationNode**: An asynchronous class that interfaces with a NATS server URL.
- **Message Handling**: Callbacks triggered by NATS subscriptions will parse the JSON payloads into ENP models and inject them into the local epistemic cycle, identical to the behavior proven in Phase 21B.1 and 21B.2.

## 4. Final Verification
This concludes Phase 21. By successfully deploying this module, the AIDP platform achieves its ultimate objective: A federated, truth-seeking collective intelligence that scales horizontally without compromising local independence.
