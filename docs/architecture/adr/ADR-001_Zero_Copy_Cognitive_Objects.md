# ADR-001: Zero-Copy Serialization with Cap'n Proto for Cognitive Objects

**Date:** 2026-07-05
**Status:** Accepted

## Context
During Milestone 7, the system required a standardized format for transferring "Cognitive Objects" (chunked textual knowledge mapped to exact source provenance) between the parsing, embedding, and storage subsystems. Originally, Python dictionaries serialized to JSON were considered. However, the system requires extreme throughput for distributed Ray clusters, and JSON deserialization overhead becomes a bottleneck for large context windows and vector payloads.

## Decision
We adopted **Cap'n Proto** (via `pycapnp`) as the canonical serialization format for all Cognitive Objects.

## Alternatives Considered
- **JSON**: Too slow, high serialization overhead, weak typing.
- **Protocol Buffers (Protobuf)**: Better typing, but still requires a decoding step to instantiate objects in memory.
- **Apache Arrow**: Excellent for columnar data, but slightly too heavy for individual nested document schemas (Provenance + Payload).

## Consequences
- **Positive**: We achieve near zero-copy deserialization. Data is read directly from memory-mapped bytes.
- **Negative**: `pycapnp` binds the lifecycle of the object strictly to the byte stream. This caused `use-after-free` segfaults when returning deserialized objects outside a context manager, forcing us to implement `DictWrapper` workarounds at the boundaries.
- **Negative**: The toolchain is more complex, requiring schema compilation (`.capnp` files).

## Validation Evidence
- **Benchmark Gate 5 (Performance)** demonstrated serialization latency of <0.4ms and identical byte reconstruction.
- **Benchmark Gate 6 (Failures)** proved that malformed byte streams raise explicit `KjException` bounds-checking errors rather than silently corrupting memory.

## Related Documents
- `015_CANONICAL_KNOWLEDGE_MODEL.md`
- `tests/benchmarks/test_gate_5_performance.py`
