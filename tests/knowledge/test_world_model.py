import pytest

from aidp.knowledge.provenance import ProvenanceEntry
from aidp.knowledge.world_model import ExperimentalResult, ScientificEntity, ScientificRelationship


def test_scientific_entity_validation() -> None:
    entity = ScientificEntity(name="p53", semantic_type="Gene")
    entity.validate()

    with pytest.raises(ValueError):
        ScientificEntity(name="", semantic_type="Gene").validate()


def test_scientific_relationship_requires_provenance() -> None:
    prov = ProvenanceEntry(claim_text="p53 inhibits tumor growth", source_paper_doi="10.1111/abc")
    rel = ScientificRelationship(
        source_entity_id="e1", target_entity_id="e2", relation_type="Inhibits", provenance=prov
    )
    rel.validate()


def test_scientific_relationship_fails_without_provenance() -> None:
    with pytest.raises(
        ValueError,
        match="Epistemic Violation: ScientificRelationship must have a valid ProvenanceEntry",
    ):
        rel = ScientificRelationship(
            source_entity_id="e1", target_entity_id="e2", relation_type="Inhibits", provenance=None
        )
        rel.validate()


def test_experimental_result_requires_provenance() -> None:
    prov = ProvenanceEntry(
        claim_text="Experiment showed inhibition", source_paper_doi="10.1111/xyz"
    )
    res = ExperimentalResult(description="Assay for p53", methodology="In vitro", provenance=prov)
    res.validate()
