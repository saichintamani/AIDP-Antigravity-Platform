import pytest

from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import deserialize_cognitive_object
from aidp.knowledge.storage import KnowledgeStorage


def test_gate_6_failures() -> None:
    """
    Gate 6: Failure Testing.
    Injects failures (corrupted binaries, bad vectors) and tests recovery.
    """
    embedder = EmbeddingService()
    storage = KnowledgeStorage()

    # 1. Truncated Cap'n Proto Object
    corrupted_bytes = b"\x00\x01\x02"  # Not a valid capnp message

    with pytest.raises(Exception):
        # Should raise some form of parsing error (likely capnp.lib.capnp.KjException or struct error)
        deserialize_cognitive_object(corrupted_bytes)

    # 2. Vector DB unavailable simulated
    # If we pass a vector of the wrong dimension, Qdrant raises an exception
    bad_vector = [0.0] * 10  # Schema expects 384

    with pytest.raises(Exception):
        storage.store_cognitive_object(b"dummy", bad_vector, "doc-bad")

    # 3. Empty document chunk
    empty_text = ""
    # Should embedder handle empty text gracefully? Yes, typically returns zero vector or valid embedding of empty string.
    try:
        v_empty = embedder.embed_text(empty_text)
        assert len(v_empty) == 384
    except Exception as e:
        pytest.fail(f"Embedding failed on empty string: {e}")

    # 4. Retrieval with wrong dimension
    with pytest.raises(Exception):
        storage.search(bad_vector, limit=1)
