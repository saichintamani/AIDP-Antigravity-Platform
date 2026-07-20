---
Document ID: AIDP-SPEC-027
Title: Phase 21B.1 - WebSocket Federation Prototype
Version: 1.0
Status: Active
---

# Phase 21B.1: WebSocket Federation Prototype

## 1. Mission Statement
Implement the physical transport layer for the Epistemic Network Protocol (ENP) using a local WebSocket mesh. Prove that disparate nodes can exchange evidence and dynamically update their Verification Statuses without humans in the loop, while adhering to ENP boundary restrictions.

## 2. Architecture
The prototype is a peer-to-peer (P2P) mesh designed for 5-20 nodes.
- **WebSocketFederationNode**: An asynchronous process wrapper around the Phase 21A `FederationNode`.
- **Server Role**: Each node binds to a local port (e.g., 8001, 8002) and listens for incoming ENP payloads.
- **Client Role**: Each node can dial out to known peer WebSockets to broadcast knowledge.

## 3. Asynchronous Routing
Incoming JSON strings are deserialized back into ENP Pydantic primitives (`EvidenceBroadcast`, `ClaimBroadcast`, etc.).
- When an `EvidenceBroadcast` is received, it is forwarded to the underlying `FederationNode` where the local Verifier uses it to resolve pending claims.

## 4. Dependencies
- Python `websockets` package
- `asyncio`

## 5. Next Steps
Once this prototype succeeds, we transition to Phase 21B.2 (Multi-Node Collective Experiments) to benchmark the emergent intelligence on real scientific data splits.
