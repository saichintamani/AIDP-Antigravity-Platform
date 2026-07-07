from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import (
    Provenance,
    deserialize_cognitive_object,
    serialize_to_cognitive_object,
)
from aidp.knowledge.storage import KnowledgeStorage


def test_gate_1_functional_pipeline() -> None:
    """
    Gate 1: Functional Validation.
    Demonstrates that the full pipeline works:
    Document -> Parser -> Chunker -> Embedding -> Canonical Object -> Vector Store -> Retrieval -> Citation Reconstruction.
    """
    embedder = EmbeddingService()
    storage = KnowledgeStorage()

    # Simulate parsed and chunked document
    doc_id = "doc-full-e2e-001"
    chunks = [
        "The first law of thermodynamics states that energy cannot be created or destroyed.",
        "The second law of thermodynamics states that entropy of an isolated system always increases.",
        "Quantum entanglement allows particles to be correlated over large distances.",
    ]

    # 1. Ingestion Pipeline
    for i, chunk_text in enumerate(chunks):
        # 1a. Provenance Tracking
        prov = Provenance(
            document_id=doc_id,
            page_number=1,
            paragraph_id=f"p-{i}",
            offset_start=0,
            offset_end=len(chunk_text),
            chunk_index=i,
            document_sha256="abc123hash",
            knowledge_score=95.0,
        )

        # 1b. Embedding
        vector = embedder.embed_text(chunk_text)

        # 1c. Canonical Object Serialization
        capnp_bytes = serialize_to_cognitive_object(chunk_text, prov)

        # 1d. Vector Store Insertion
        storage.store_cognitive_object(capnp_bytes, vector, doc_id)

    assert storage.count() == 3

    # 2. Retrieval Pipeline
    query = "What happens to entropy in a closed system?"
    query_vector = embedder.embed_text(query)

    # 2a. Vector Search
    results = storage.search(query_vector, limit=1)
    assert len(results) == 1

    # 2b. Citation Reconstruction
    retrieved_bytes = bytes.fromhex(results[0]["capnp_data"])
    reconstructed = deserialize_cognitive_object(retrieved_bytes)

    assert reconstructed.documentId == doc_id
    assert reconstructed.chunkIndex == 1
    assert "entropy of an isolated system" in reconstructed.payload
    assert reconstructed.knowledgeScore == 95.0
    assert reconstructed.documentSha256 == "abc123hash"
