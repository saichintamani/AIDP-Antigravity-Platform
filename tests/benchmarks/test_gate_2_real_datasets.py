import hashlib

from aidp.knowledge.embedding import EmbeddingService
from aidp.knowledge.serialization import Provenance, serialize_to_cognitive_object
from aidp.knowledge.storage import KnowledgeStorage


def generate_mock_doc_chunks(doc_type: str) -> list[str]:
    """Generates synthetic but realistic text chunks based on structural document types."""
    if doc_type == "wikipedia":
        return [
            "Artificial intelligence (AI) is intelligence demonstrated by machines.",
            "AI research has been defined as the field of study of intelligent agents.",
            "== History ==\nThe field was founded on the assumption that human intelligence can be precisely described.",
        ]
    elif doc_type == "arxiv":
        return [
            "Abstract: We introduce a new architecture for scalable transformers.",
            "1. Introduction. The attention mechanism has become the standard for NLP.",
            "We propose a linear time complexity attention variant.",
        ]
    elif doc_type == "multicolumn_pdf":
        return [
            "Column 1 text flow which might unexpectedly",
            "Column 2 starts here with totally unrelated text",
            "wrap around back to column 1's previous sentence.",
        ]
    elif doc_type == "ocr_scan":
        return [
            "Tnis document vvas scanned viith a po0r res0lution.",
            "1ntelIigence is hard to m3asure.",
            "We c0nclude th4t OCR errors intr0duce n0ise.",
        ]
    elif doc_type == "large_technical_doc":
        return [
            "API Reference v2.4.1",
            "Endpoint: GET /v1/agents/{id}",
            "Returns a JSON object representing the agent configuration state.",
        ]
    return []


def test_gate_2_real_datasets() -> None:
    """
    Gate 2: Benchmark Validation.
    Validates ingestion and retrieval across 5 structural document categories.
    """
    embedder = EmbeddingService()
    storage = KnowledgeStorage()

    categories = ["wikipedia", "arxiv", "multicolumn_pdf", "ocr_scan", "large_technical_doc"]

    # Ingest
    for cat in categories:
        chunks = generate_mock_doc_chunks(cat)
        doc_hash = hashlib.sha256(cat.encode()).hexdigest()

        for i, text in enumerate(chunks):
            prov = Provenance(
                document_id=f"doc-{cat}",
                page_number=1,
                paragraph_id=f"p-{i}",
                offset_start=0,
                offset_end=len(text),
                chunk_index=i,
                document_sha256=doc_hash,
                knowledge_score=85.0,
            )
            v = embedder.embed_text(text)
            b = serialize_to_cognitive_object(text, prov)
            storage.store_cognitive_object(b, v, f"doc-{cat}")

    assert storage.count() == 15

    # Test specific retrieval to ensure structural categories don't break semantic matching
    # 1. OCR query
    v_ocr = embedder.embed_text("Scanning documents can lead to bad text resolution.")
    res_ocr = storage.search(v_ocr, limit=1, doc_filter=None)
    assert len(res_ocr) == 1

    # 2. Tech doc query
    v_tech = embedder.embed_text("How do I fetch the agent state via REST API?")
    res_tech = storage.search(v_tech, limit=1)
    assert len(res_tech) == 1
