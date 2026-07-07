from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import Provenance, serialize_to_cognitive_object
from aidp.knowledge.storage import KnowledgeStorage


def execute_pipeline(
    embedder: EmbeddingService, storage: KnowledgeStorage, doc_id: str, text: str
) -> tuple[list[float], bytes, str]:
    """Runs a single chunk through the pipeline and returns the intermediate determinisitic artifacts."""
    # 1. Provenance
    prov = Provenance(
        document_id=doc_id,
        page_number=1,
        paragraph_id="p0",
        offset_start=0,
        offset_end=len(text),
        chunk_index=0,
        document_sha256="abc",
        knowledge_score=100.0,
    )

    # 2. Embed
    vector = embedder.embed_text(text)

    # 3. Serialize
    # Serialization uses timestamp, which breaks exact reproducibility of bytes.
    # We will verify the semantic parts.
    capnp_bytes = serialize_to_cognitive_object(text, prov)

    # 4. Store
    point_id = storage.store_cognitive_object(capnp_bytes, vector, doc_id)

    return vector, capnp_bytes, point_id


def test_gate_7_reproducibility() -> None:
    """
    Gate 7: Reproducibility.
    Executes the pipeline twice and verifies embeddings, rankings, and provenance match.
    """
    embedder1 = EmbeddingService()
    embedder2 = EmbeddingService()

    storage1 = KnowledgeStorage()
    storage2 = KnowledgeStorage()

    text = "Machine learning models must yield reproducible results to be scientifically valid."

    v1, b1, p1 = execute_pipeline(embedder1, storage1, "doc-rep-1", text)
    v2, b2, p2 = execute_pipeline(embedder2, storage2, "doc-rep-1", text)

    # 1. Vectors must be perfectly identical
    assert v1 == v2, "Embeddings are non-deterministic"

    # 2. Retrieval matching
    q = "Why is reproducibility important?"
    q_vec = embedder1.embed_text(q)

    res1 = storage1.search(q_vec, limit=1)
    res2 = storage2.search(q_vec, limit=1)

    assert len(res1) == 1
    assert len(res2) == 1

    # 3. Check exact provenance matching
    from aidp.knowledge.serialization import deserialize_cognitive_object

    rec1 = deserialize_cognitive_object(bytes.fromhex(res1[0]["capnp_data"]))
    rec2 = deserialize_cognitive_object(bytes.fromhex(res2[0]["capnp_data"]))

    assert rec1.documentId == rec2.documentId
    assert rec1.offsetStart == rec2.offsetStart
    assert rec1.chunkIndex == rec2.chunkIndex
    assert rec1.payload == rec2.payload
