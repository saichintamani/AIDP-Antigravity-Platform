import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ProvenanceEntry:
    """
    The cornerstone of epistemic traceability in AIDP.
    Tracks the exact origin and extraction metadata of every scientific statement.
    """

    claim_text: str
    source_paper_doi: str | None = None
    source_url: str | None = None
    retriever_metadata: dict[str, Any] = field(default_factory=dict)
    provider_metadata: dict[str, Any] = field(default_factory=dict)
    workflow_timestamp: float = field(default_factory=time.time)
    reviewer_comments: dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0
    id: str = field(default_factory=lambda: f"prov_{uuid.uuid4()}")

    def calculate_replay_hash(self) -> str:
        """
        Creates a deterministic hash of the provenance state to guarantee replayability.
        """
        data = {
            "claim": self.claim_text,
            "source_doi": self.source_paper_doi,
            "provider": self.provider_metadata.get("model_name", "unknown"),
        }
        encoded = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def validate(self) -> None:
        """Ensures the provenance entry has minimum acceptable trace evidence."""
        if not self.claim_text:
            raise ValueError("ProvenanceEntry must contain the claim text.")
        if not self.source_paper_doi and not self.source_url:
            raise ValueError("ProvenanceEntry must trace back to a DOI or URL source.")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
