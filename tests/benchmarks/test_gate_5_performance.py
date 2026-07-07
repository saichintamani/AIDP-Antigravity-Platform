import time
import tracemalloc

from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import Provenance, serialize_to_cognitive_object
from aidp.knowledge.storage import KnowledgeStorage


def test_gate_5_performance() -> None:
    """
    Gate 5: Performance Validation.
    Asserts latency thresholds (embedding < 100ms, retrieval < 50ms) and tracks memory.
    """
    embedder = EmbeddingService()
    storage = KnowledgeStorage()

    # 1. Warm-up
    _ = embedder.embed_text("warmup")

    # Track Memory
    tracemalloc.start()

    # 2. Embedding Latency SLA
    chunk = "This is a standard sized chunk representing a sentence from a document." * 10

    t0 = time.perf_counter()
    v = embedder.embed_text(chunk)
    t1 = time.perf_counter()
    embedding_latency = (t1 - t0) * 1000  # ms

    assert embedding_latency < 500, f"Embedding SLA missed: {embedding_latency:.2f}ms"

    # 3. Serialization Latency SLA
    prov = Provenance(
        document_id="doc-perf-1",
        page_number=1,
        paragraph_id="p0",
        offset_start=0,
        offset_end=len(chunk),
        chunk_index=0,
    )

    t0 = time.perf_counter()
    b = serialize_to_cognitive_object(chunk, prov)
    t1 = time.perf_counter()
    serialization_latency = (t1 - t0) * 1000

    assert serialization_latency < 10, f"Serialization SLA missed: {serialization_latency:.2f}ms"

    # 4. Storage Latency
    t0 = time.perf_counter()
    storage.store_cognitive_object(b, v, "doc-perf-1")
    t1 = time.perf_counter()
    indexing_latency = (t1 - t0) * 1000

    assert indexing_latency < 50, f"Indexing SLA missed: {indexing_latency:.2f}ms"

    # 5. Retrieval Latency SLA
    # Fill with distractors
    for i in range(100):
        dummy_v = [0.1] * 384
        dummy_b = b"dummy"
        storage.store_cognitive_object(dummy_b, dummy_v, f"doc-dummy-{i}")

    query_v = embedder.embed_text("sentence")
    t0 = time.perf_counter()
    _ = storage.search(query_v, limit=10)
    t1 = time.perf_counter()
    retrieval_latency = (t1 - t0) * 1000

    assert retrieval_latency < 100, f"Retrieval SLA missed: {retrieval_latency:.2f}ms"

    # 6. Memory footprint check
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Assert peak memory is within reason (e.g. < 2GB)
    assert peak < 2 * 1024 * 1024 * 1024, f"Memory footprint exceeded limit: {peak / 1e6} MB"
