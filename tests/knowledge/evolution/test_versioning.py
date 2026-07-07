from aidp.knowledge.evolution.versioning import SnapshotManager
from aidp.knowledge.world_model import ScientificEntity


def test_snapshot_creation_immutability() -> None:
    manager = SnapshotManager()

    # Commit first change
    e1 = ScientificEntity(name="p53", semantic_type="Gene")
    v1 = manager.commit_changes("Added p53", new_entities=[e1])

    assert v1.version_id == "v2.0"
    assert len(v1.entities) == 1

    # Commit second change
    e2 = ScientificEntity(name="Cancer", semantic_type="Disease")
    v2 = manager.commit_changes("Added Cancer", new_entities=[e2])

    assert v2.version_id == "v3.0"
    assert len(v2.entities) == 2

    # Verify v1 was not modified (Immutability)
    assert len(v1.entities) == 1
    assert v2.parent_version_id == "v2.0"
