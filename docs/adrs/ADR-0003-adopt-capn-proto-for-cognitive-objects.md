# ADR 0003: Adopt Cap'n Proto for Canonical Cognitive Objects

## Context
The platform strictly mandates a Canonical Cognitive Object to prevent semantic fragmentation between the Agent Core, Knowledge Substrate, and Mathematical Engine.

## Decision
We will adopt **Cap'n Proto** as the serialization protocol for active, in-memory Cognitive Objects, reserving Apache Arrow exclusively for bulk vector storage.

## Status
Approved

## Consequences
*   **Positive:** Cap'n Proto provides true zero-copy serialization. When Ray Actors pass complex, deeply nested hypothesis trees over the network, there is zero parsing overhead.
*   **Negative:** Cap'n Proto lacks the vast data-science ecosystem support of Pandas/Arrow, requiring custom deserialization boundaries when interacting with standard ML plotting libraries.

## Alternatives Considered
*   **Apache Arrow:** Rejected for *active memory*. Arrow is an immutable, columnar OLAP format, highly inefficient for deeply nested, mutating cognitive DAGs.
*   **JSON / Protobuf:** Rejected. Protobuf requires costly deserialization/parsing at every Ray Actor hop. JSON is untyped and highly bloated.
