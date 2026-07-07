from aidp.knowledge.evolution.belief_revision import BeliefReviser
from aidp.knowledge.provenance import ProvenanceEntry
from aidp.knowledge.world_model import ScientificRelationship


def test_belief_revision_fusion() -> None:
    reviser = BeliefReviser()

    prov1 = ProvenanceEntry(claim_text="Paper 1", confidence_score=0.6)
    rel1 = ScientificRelationship(
        source_entity_id="e1", target_entity_id="e2", relation_type="Inhibits", provenance=prov1
    )

    prov2 = ProvenanceEntry(claim_text="Paper 2", confidence_score=0.7)
    rel2 = ScientificRelationship(
        source_entity_id="e1", target_entity_id="e2", relation_type="Inhibits", provenance=prov2
    )

    revised_rel = reviser.revise_belief(rel1, rel2)

    # Cumulative fusion of 0.6 and 0.7 should yield a higher belief
    assert revised_rel.provenance.confidence_score > 0.7
    assert revised_rel.relation_type == "Inhibits"
    assert "revision_history" in revised_rel.provenance.provider_metadata
