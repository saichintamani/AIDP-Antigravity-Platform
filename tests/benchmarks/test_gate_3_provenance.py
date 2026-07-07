import hashlib

from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import (
    Provenance,
    deserialize_cognitive_object,
    serialize_to_cognitive_object,
)
from aidp.knowledge.storage import KnowledgeStorage


def test_gate_3_provenance_validation() -> None:
    """
    Gate 3: Provenance Validation.
    Asserts that every retrieved fact perfectly reconstructs:
    Document -> SHA256 -> Page -> Paragraph -> Character Offset -> Chunk -> Embedding -> Retrieval.
    """
    embedder = EmbeddingService()
    storage = KnowledgeStorage()

    # 1. Document definition
    raw_document = (
        "Artificial Intelligence Discovery Platform (AIDP) validates scientific architectures."
    )
    doc_id = "doc-prov-001"
    doc_sha256 = hashlib.sha256(raw_document.encode()).hexdigest()

    # 2. Page & Paragraph definition
    page = 42
    paragraph = "p-99"
    offset_start = 0
    offset_end = len(raw_document)
    chunk_index = 0

    # 3. Provenance formulation
    prov = Provenance(
        document_id=doc_id,
        page_number=page,
        paragraph_id=paragraph,
        offset_start=offset_start,
        offset_end=offset_end,
        chunk_index=chunk_index,
        document_sha256=doc_sha256,
        knowledge_score=99.9,
    )

    # 4. Embedding & Serialization
    vector = embedder.embed_text(raw_document)
    capnp_bytes = serialize_to_cognitive_object(raw_document, prov)

    # 5. Storage
    storage.store_cognitive_object(capnp_bytes, vector, doc_id)

    # 6. Retrieval
    query_vector = embedder.embed_text("AIDP architecture validation")
    results = storage.search(query_vector, limit=1)
    assert len(results) == 1

    # 7. Exact Provenance Reconstruction
    retrieved_bytes = bytes.fromhex(results[0]["capnp_data"])
    reconstructed = deserialize_cognitive_object(retrieved_bytes)

    assert reconstructed.documentId == doc_id, "Document ID mismatch"
    assert reconstructed.documentSha256 == doc_sha256, "SHA256 mismatch"
    assert reconstructed.pageNumber == page, "Page mismatch"
    assert reconstructed.paragraphId == paragraph, "Paragraph mismatch"
    assert reconstructed.offsetStart == offset_start, "Offset Start mismatch"
    assert reconstructed.offsetEnd == offset_end, "Offset End mismatch"
    assert reconstructed.chunkIndex == chunk_index, "Chunk Index mismatch"
    assert reconstructed.payload == raw_document, "Payload mismatch"
    assert abs(reconstructed.knowledgeScore - 99.9) < 1e-5, "Knowledge Score mismatch"
