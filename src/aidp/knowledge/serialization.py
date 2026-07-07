import time
import uuid
from pathlib import Path

import capnp  # type: ignore[import-untyped]

SCHEMA_DIR = Path(__file__).parent.parent / "core" / "schemas"
COGNITIVE_OBJECT_SCHEMA = SCHEMA_DIR / "cognitive_object.capnp"

from dataclasses import dataclass


@dataclass
class Provenance:
    document_id: str
    page_number: int
    paragraph_id: str
    offset_start: int
    offset_end: int
    chunk_index: int
    document_sha256: str = ""
    knowledge_score: float = 0.0


def serialize_to_cognitive_object(payload: str, provenance: Provenance) -> bytes:
    """Serializes a raw text payload into a binary Cap'n Proto Cognitive Object."""
    if not COGNITIVE_OBJECT_SCHEMA.exists():
        raise FileNotFoundError(f"Schema not found: {COGNITIVE_OBJECT_SCHEMA}")

    cognitive_object_capnp = capnp.load(str(COGNITIVE_OBJECT_SCHEMA))

    obj = cognitive_object_capnp.CognitiveObject.new_message()
    obj.id = str(uuid.uuid4())
    obj.documentId = provenance.document_id
    obj.pageNumber = provenance.page_number
    obj.paragraphId = provenance.paragraph_id
    obj.offsetStart = provenance.offset_start
    obj.offsetEnd = provenance.offset_end
    obj.chunkIndex = provenance.chunk_index
    obj.payload = payload
    obj.timestamp = time.time()
    obj.documentSha256 = provenance.document_sha256
    obj.knowledgeScore = provenance.knowledge_score

    return bytes(obj.to_bytes())


from typing import Any


class DictWrapper:
    def __init__(self, data_dict: dict[str, Any]) -> None:
        self.__dict__.update(data_dict)


def deserialize_cognitive_object(data: bytes) -> Any:
    """Deserializes a binary Cap'n Proto Cognitive Object."""
    cognitive_object_capnp = capnp.load(str(COGNITIVE_OBJECT_SCHEMA))

    reader = cognitive_object_capnp.CognitiveObject.from_bytes(data)
    if hasattr(reader, "__enter__"):
        with reader as obj:
            return DictWrapper(obj.to_dict())
    else:
        return reader
