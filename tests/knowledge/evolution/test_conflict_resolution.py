from aidp.knowledge.evolution.conflict_resolution import ContradictionDetector, DebateTrigger
from aidp.knowledge.evolution.versioning import SnapshotManager
from aidp.knowledge.provenance import ProvenanceEntry
from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship


def test_contradiction_detector() -> None:
    detector = ContradictionDetector()
    manager = SnapshotManager()

    e1 = ScientificEntity(name="A", semantic_type="Drug")
    e2 = ScientificEntity(name="B", semantic_type="Protein")

    prov_a = ProvenanceEntry(claim_text="Inhibits")
    rel_a = ScientificRelationship(e1.id, e2.id, "Inhibits", prov_a)

    prov_b = ProvenanceEntry(claim_text="Activates")
    rel_b = ScientificRelationship(e1.id, e2.id, "Activates", prov_b)

    snapshot = manager.commit_changes("Initial", [e1, e2], [rel_a, rel_b])

    conflicts = detector.detect_conflicts(snapshot)
    assert len(conflicts) == 1

    # Check DebateTrigger
    trigger = DebateTrigger(confidence_threshold=0.1)

    # Both have default confidence 0.0, diff is 0.0 <= 0.1 -> Should trigger debate
    assert trigger.should_trigger_debate(conflicts[0][0], conflicts[0][1]) is True

    # Modify confidence to avoid debate trigger
    conflicts[0][0].provenance.confidence_score = 0.9
    conflicts[0][1].provenance.confidence_score = 0.2

    assert trigger.should_trigger_debate(conflicts[0][0], conflicts[0][1]) is False
