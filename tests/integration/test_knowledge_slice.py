import os
import tempfile

import fitz  # type: ignore[import-untyped]

from aidp.knowledge.extraction import DocumentParser
from aidp.knowledge.serialization import serialize_to_cognitive_object
from aidp.knowledge.storage import KnowledgeStorage


def test_knowledge_slice_end_to_end() -> None:
    # 1. Create a dummy PDF
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)  # noqa: SIM115
    pdf_path = tmp.name
    tmp.close()

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "AIDP Empirical Validation Payload")
    doc.save(pdf_path)
    doc.close()

    try:
        parser = DocumentParser(pdf_path)
        chunks_with_prov = list(parser.parse_blocks())
        chunks = [c[0] for c in chunks_with_prov]
        assert len(chunks) > 0
        assert "AIDP Empirical Validation Payload" in chunks[0]

        # 3. Serialize into Cap'n Proto Cognitive Object
        capnp_bytes = serialize_to_cognitive_object(
            payload=chunks[0], provenance=chunks_with_prov[0][1]
        )
        assert isinstance(capnp_bytes, bytes)
        assert len(capnp_bytes) > 0

        # 4. Store in Qdrant
        storage = KnowledgeStorage()
        storage.store_cognitive_object(
            capnp_bytes=capnp_bytes,
            embedding=[0.0] * 384,
            document_id=chunks_with_prov[0][1].document_id,
        )

        # 5. Verify Storage
        assert storage.count() == 1

    finally:
        os.remove(pdf_path)
