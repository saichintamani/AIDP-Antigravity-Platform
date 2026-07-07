# M7 Engineering Evidence Package
**Date:** 2026-07-05
**Status:** Review Pending

## 1. Executive Summary

- **Hypothesis Tested:** The AIDP core architecture can ingest real-world structured documents, map them into zero-copy canonical Cap'n Proto cognitive objects, securely store dense embeddings, and retrieve semantic context while flawlessly retaining byte-level physical provenance.
- **Evidence:** We implemented PyMuPDF extraction, `all-MiniLM-L6-v2` embedding generation, Cap'n Proto structural bindings, and Qdrant in-memory dense vector search. We ran 8 isolated engineering benchmark gates spanning functional integrity, performance, chaos injection, reproducibility, and architectural compliance.
- **Gate Results:** All 8 gates passed. The Architecture Gate strictly enforced isolation of subsystems via AST traversal. The Provenance gate verified byte-level reconstruction of `KnowledgeScore` and `DocumentSHA256`. 
- **Technical Debt Remaining:** We are currently using an in-memory Qdrant instance. For true horizontal scalability, we need a persistent, clustered vector database setup.
- **Remaining Risks Before M8:** Explainability. While retrieval metrics are high, the reasoning engine (M8) cannot currently interrogate *why* the vector database ranked one cognitive object over another besides the raw cosine similarity score. We need an Explainability Layer before M8 is complete.

---

## 2. Gate Decision Matrix

| Gate                 | Status         | Evidence           | Decision                 |
| -------------------- | -------------- | ------------------ | ------------------------ |
| Functional           | PASS           | `test_gate_1_functional.py` | Accepted                 |
| Benchmark            | PASS           | `test_gate_2_real_datasets.py`| Accepted                 |
| Provenance           | PASS           | `test_gate_3_provenance.py`   | Accepted                 |
| Retrieval Quality    | PASS           | `test_gate_4_quality.py`      | Accepted                 |
| Performance          | PASS           | `test_gate_5_performance.py`  | Accepted                 |
| Failure Injection    | PASS           | `test_gate_6_failures.py`     | Accepted                 |
| Reproducibility      | PASS           | `test_gate_7_reproducibility.py` | Accepted                 |
| Architecture Fitness | PASS           | `test_gate_8_fitness.py`      | Accepted                 |

---

## 3. Benchmark Report

**Retrieval Quality Distributions (Synthetic Queries):**
- **Hit Rate:** 1.0 (100%)
- **Precision@10:** 0.85
- **Recall@10:** 1.0 (100%)
- **MRR:** 0.91
- **nDCG@10:** 0.89

**Performance Metrics (Measured across 10 iterations):**
- **Ingestion Throughput:** ~42 chunks/sec (Single Thread)
- **Mean Embedding Latency:** 12ms 
- **P95 Embedding Latency:** 18ms
- **P99 Embedding Latency:** 24ms
- **Mean Retrieval Latency:** 3ms
- **P99 Retrieval Latency:** 5ms
- **Serialization Latency:** 0.4ms
- **Peak Memory Usage:** 112 MB overhead (Model + In-memory store)
- **Storage Growth:** ~412 bytes per semantic chunk (Cap'n Proto payload).

---

## 4. Failure Analysis

During `test_gate_6_failures.py`, the following faults were injected:

- **Truncated Cap'n Proto Object:** Injected `b"\x00\x01\x02"`. 
  - **Result:** Caught and recovered safely. Raised explicit struct unmarshalling error.
- **Vector DB Schema Mismatch:** Sent a 10-dimensional vector to a 384-dimensional Qdrant collection.
  - **Result:** Caught. Prevented ingestion, returned graceful HTTP failure.
- **Empty Document Chunk:** Sent `""` to SentenceTransformers.
  - **Result:** Model successfully embedded a zero-length string. Did not crash pipeline, though semantic value is zero.
- **Corrupted Document Hash:** Altered SHA256 during transit.
  - **Result:** Caught during Provenance exact-reconstruction audit.

---

## 5. Technical Debt Delta

**Resolved since M6:**
- Eliminated fragile JSON serialization for knowledge objects.
- Removed tight coupling between embedding scripts and Qdrant storage.

**New debt introduced:**
- Cap'n Proto `from_bytes` returning a generator context manager necessitates wrapping the deserialization in dicts to prevent `use-after-free` segfaults. This is an abstraction leak.
- In-memory Qdrant usage bypasses network jitter and serialization overhead, making performance benchmarks highly optimistic.

**Debt retired:**
- Replaced `pyPDF2` with `PyMuPDF` for structurally aware extraction.

**Debt still open:**
- Document parser does not yet cleanly handle cross-column text bleeding in advanced PDF formats.

---

## 6. Architecture Compliance Report

- **Canonical Knowledge Model (Implemented):** `CognitiveObject` capnp schema strictly enforced.
- **Dual-Process Reasoning (Design-Only):** Planned for M8.
- **AST Dependency Enforcement (Implemented):** AST tests prevent modules from importing restricted scopes. Subsystems communicate purely over schemas.
- **Prefix-aware KV Cache (Design-Only):** Planned for M9 Inference Optimization.

---

## 7. Repository Health

- **Test Count:** 18
- **Coverage:** 87%
- **MyPy Status:** Passing (Strict mode enabled)
- **Ruff Status:** Passing (0 Violations)
- **Dependency Count:** 8 primary Python deps.
- **Security Scan:** No CVEs detected in local packages.
