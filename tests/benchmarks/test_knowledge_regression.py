
import pytest

from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import (
    Provenance,
    deserialize_cognitive_object,
    serialize_to_cognitive_object,
)
from aidp.knowledge.storage import KnowledgeStorage


# Setup fixture
@pytest.fixture
def knowledge_system() -> tuple[EmbeddingService, KnowledgeStorage]:
    embedding_service = EmbeddingService()
    storage = KnowledgeStorage()
    return embedding_service, storage


def test_provenance_integrity(knowledge_system: tuple[EmbeddingService, KnowledgeStorage]) -> None:
    """Verifies that a stored object perfectly retains its provenance chain on retrieval."""
    embedder, storage = knowledge_system

    # 1. Create a dummy chunk
    text = "The quick brown fox jumps over the lazy dog. This is a scientific fact."
    prov = Provenance(
        document_id="doc-tier1-001",
        page_number=1,
        paragraph_id="p-001",
        offset_start=0,
        offset_end=len(text),
        chunk_index=0,
    )

    # 2. Embed and Serialize
    vector = embedder.embed_text(text)
    capnp_bytes = serialize_to_cognitive_object(text, prov)

    # 3. Store
    storage.store_cognitive_object(capnp_bytes, vector, prov.document_id)

    # 4. Search
    results = storage.search(vector, limit=1)
    assert len(results) == 1

    # 5. Reconstruct Provenance
    retrieved_bytes = bytes.fromhex(results[0]["capnp_data"])
    reconstructed = deserialize_cognitive_object(retrieved_bytes)

    assert reconstructed.payload == text
    assert reconstructed.documentId == prov.document_id
    assert reconstructed.pageNumber == prov.page_number
    assert reconstructed.paragraphId == prov.paragraph_id
    assert reconstructed.offsetStart == prov.offset_start
    assert reconstructed.offsetEnd == prov.offset_end
    assert reconstructed.chunkIndex == prov.chunk_index


def test_recall_at_1(knowledge_system: tuple[EmbeddingService, KnowledgeStorage]) -> None:
    """Tests the semantic retrieval capability using dense vectors."""
    embedder, storage = knowledge_system

    # Insert distractor facts
    distractors = [
        "The sky is blue because of Rayleigh scattering.",
        "Mitochondria is the powerhouse of the cell.",
        "Photosynthesis converts light into chemical energy.",
    ]
    for i, d in enumerate(distractors):
        v = embedder.embed_text(d)
        p = Provenance("doc-distract", 1, str(i), 0, len(d), i)
        b = serialize_to_cognitive_object(d, p)
        storage.store_cognitive_object(b, v, "doc-distract")

    # Insert target fact
    target = "Agent reasoning loops require metacognition."
    target_v = embedder.embed_text(target)
    target_p = Provenance("doc-target", 1, "0", 0, len(target), 0)
    target_b = serialize_to_cognitive_object(target, target_p)
    storage.store_cognitive_object(target_b, target_v, "doc-target")

    # Query with a semantic variant
    query = "Why do agents need to think about their own thinking?"
    query_v = embedder.embed_text(query)

    results = storage.search(query_v, limit=1)
    retrieved_bytes = bytes.fromhex(results[0]["capnp_data"])
    reconstructed = deserialize_cognitive_object(retrieved_bytes)

    assert reconstructed.payload == target
