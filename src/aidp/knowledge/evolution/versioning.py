import hashlib
import json
import time
from dataclasses import dataclass

from aidp.knowledge.world_model import ScientificEntity, ScientificRelationship


@dataclass
class WorldStateSnapshot:
    """
    Represents an immutable version of the World Model at a specific point in time.
    """

    version_id: str
    parent_version_id: str | None
    timestamp: float
    reason: str
    entities: dict[str, ScientificEntity]
    relationships: dict[str, ScientificRelationship]

    def calculate_hash(self) -> str:
        data = {
            "version": self.version_id,
            "parent": self.parent_version_id,
            "entities": sorted(self.entities.keys()),
            "relationships": sorted(self.relationships.keys()),
        }
        encoded = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class SnapshotManager:
    """
    Manages the Git-like history of the World Model.
    Never overwrites data, always appends new snapshots.
    """

    def __init__(self) -> None:
        self.snapshots: dict[str, WorldStateSnapshot] = {}
        self.head_version_id: str | None = None
        self.version_counter = 0

        # Create genesis snapshot
        self._create_snapshot("Genesis", {}, {})

    def _create_snapshot(
        self,
        reason: str,
        entities: dict[str, ScientificEntity],
        relationships: dict[str, ScientificRelationship],
    ) -> WorldStateSnapshot:
        self.version_counter += 1
        new_version_id = f"v{self.version_counter}.0"

        snapshot = WorldStateSnapshot(
            version_id=new_version_id,
            parent_version_id=self.head_version_id,
            timestamp=time.time(),
            reason=reason,
            entities=entities.copy(),
            relationships=relationships.copy(),
        )

        self.snapshots[new_version_id] = snapshot
        self.head_version_id = new_version_id
        return snapshot

    def get_head(self) -> WorldStateSnapshot:
        if not self.head_version_id:
            raise RuntimeError("No snapshots exist.")
        return self.snapshots[self.head_version_id]

    def commit_changes(
        self,
        reason: str,
        new_entities: list[ScientificEntity] | None = None,
        new_relationships: list[ScientificRelationship] | None = None,
    ) -> WorldStateSnapshot:
        """
        Creates a new snapshot by combining the current head with the new entities and relationships.
        """
        head = self.get_head()

        updated_entities = head.entities.copy()
        if new_entities:
            for entity in new_entities:
                updated_entities[entity.id] = entity

        updated_relationships = head.relationships.copy()
        if new_relationships:
            for rel in new_relationships:
                updated_relationships[rel.id] = rel

        return self._create_snapshot(reason, updated_entities, updated_relationships)
