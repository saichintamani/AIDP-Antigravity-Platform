import pytest

from aidp.knowledge.provenance import ProvenanceEntry


def test_provenance_entry_validation_success() -> None:
    entry = ProvenanceEntry(claim_text="X inhibits Y", source_paper_doi="10.1000/xyz123")
    # Should not raise exception
    entry.validate()


def test_provenance_entry_validation_missing_claim() -> None:
    entry = ProvenanceEntry(claim_text="", source_paper_doi="10.1000/xyz123")
    with pytest.raises(ValueError, match="ProvenanceEntry must contain the claim text."):
        entry.validate()


def test_provenance_entry_validation_missing_source() -> None:
    entry = ProvenanceEntry(claim_text="X inhibits Y")
    with pytest.raises(ValueError, match="ProvenanceEntry must trace back to a DOI or URL source."):
        entry.validate()


def test_provenance_replay_hash_determinism() -> None:
    entry1 = ProvenanceEntry(
        claim_text="X inhibits Y",
        source_paper_doi="10.1000/xyz123",
        provider_metadata={"model_name": "gemini-1.5-pro"},
    )

    entry2 = ProvenanceEntry(
        claim_text="X inhibits Y",
        source_paper_doi="10.1000/xyz123",
        provider_metadata={"model_name": "gemini-1.5-pro"},
    )

    assert entry1.calculate_replay_hash() == entry2.calculate_replay_hash()


def test_provenance_replay_hash_difference() -> None:
    entry1 = ProvenanceEntry(
        claim_text="X inhibits Y",
        source_paper_doi="10.1000/xyz123",
        provider_metadata={"model_name": "gemini-1.5-pro"},
    )

    entry2 = ProvenanceEntry(
        claim_text="X inhibits Y",
        source_paper_doi="10.1000/xyz123",
        provider_metadata={"model_name": "gpt-4"},
    )

    assert entry1.calculate_replay_hash() != entry2.calculate_replay_hash()
