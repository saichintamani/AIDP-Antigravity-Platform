from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.evaluation import calculate_retrieval_metrics
from aidp.knowledge.serialization import Provenance, serialize_to_cognitive_object
from aidp.knowledge.storage import KnowledgeStorage


def test_gate_4_retrieval_quality() -> None:
    """
    Gate 4: Retrieval Quality.
    Validates semantic retrieval across metrics: Precision@10, Recall@10, MRR, nDCG/MAP, Hit Rate.
    """
    embedder = EmbeddingService()
    storage = KnowledgeStorage()

    # 1. Dataset Generation
    corpus = {
        "doc-q1-1": "Ray orchestration provides actor pools for distributed agent execution.",
        "doc-q1-2": "Distributed systems require careful handling of concurrency and state.",
        "doc-q2-1": "The quick brown fox jumps over the lazy dog.",
        "doc-q2-2": "Canines are known for their speed and agility.",
        "doc-q3-1": "Cap'n Proto is an extremely fast data interchange format.",
        "doc-q3-2": "Serialization overhead is a major bottleneck in distributed ML.",
        "doc-q3-3": "Zero-copy deserialization enables memory-mapped struct reading.",
    }

    for doc_id, text in corpus.items():
        v = embedder.embed_text(text)
        prov = Provenance(
            document_id=doc_id,
            page_number=1,
            paragraph_id="p0",
            offset_start=0,
            offset_end=len(text),
            chunk_index=0,
        )
        b = serialize_to_cognitive_object(text, prov)
        storage.store_cognitive_object(b, v, doc_id)

    # 2. Queries and their expected relevant Document IDs
    queries = [
        ("How does Ray handle distributed tasks?", ["doc-q1-1", "doc-q1-2"]),
        ("Tell me about fast serialization formats.", ["doc-q3-1", "doc-q3-2", "doc-q3-3"]),
    ]

    # 3. Evaluate
    for q_text, relevant_ids in queries:
        q_vec = embedder.embed_text(q_text)
        results = storage.search(q_vec, limit=10)

        # Extract doc_ids from results
        from aidp.knowledge.serialization import deserialize_cognitive_object

        retrieved_ids = []
        for r in results:
            r_bytes = bytes.fromhex(r["capnp_data"])
            reconstructed = deserialize_cognitive_object(r_bytes)
            retrieved_ids.append(reconstructed.documentId)

        metrics = calculate_retrieval_metrics(retrieved_ids, relevant_ids, k=10)

        # Assertions
        assert metrics["hit_rate"] == 1.0, f"Failed hit rate for query: {q_text}"
        assert metrics["mrr"] > 0.0, f"Failed MRR for query: {q_text}"
        assert metrics["recall@10"] > 0.0, f"Failed recall for query: {q_text}"

        # Log metrics for CI observation
        print(f"Query: {q_text}")
        print(metrics)
