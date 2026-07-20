
from aidp.knowledge.evolution.versioning import WorldStateSnapshot
from aidp.knowledge.world_model import ScientificRelationship


class ContradictionDetector:
    """
    Scans the World Model for conflicting claims (e.g. A inhibits B vs A activates B).
    """

    # Simple explicit contradiction map for demonstration
    CONTRADICTION_MAP = {
        "Inhibits": ["Activates", "Upregulates", "Enhances"],
        "Activates": ["Inhibits", "Downregulates", "Suppresses"],
        "Causes": ["Prevents", "Cures"],
    }

    def detect_conflicts(
        self, snapshot: WorldStateSnapshot
    ) -> list[tuple[ScientificRelationship, ScientificRelationship]]:
        conflicts = []

        # Group by edge pair
        edge_groups: dict[tuple[str, str], list[ScientificRelationship]] = {}
        for rel in snapshot.relationships.values():
            key = (rel.source_entity_id, rel.target_entity_id)
            if key not in edge_groups:
                edge_groups[key] = []
            edge_groups[key].append(rel)

        # Detect contradictions within groups
        for edges in edge_groups.values():
            if len(edges) < 2:
                continue

            for i in range(len(edges)):
                for j in range(i + 1, len(edges)):
                    rel_a = edges[i]
                    rel_b = edges[j]

                    if rel_b.relation_type in self.CONTRADICTION_MAP.get(rel_a.relation_type, []):
                        conflicts.append((rel_a, rel_b))

        return conflicts


class DebateTrigger:
    """
    Evaluates detected conflicts to determine if they warrant a full Scientific Debate.
    """

    def __init__(self, confidence_threshold: float = 0.1) -> None:
        # Trigger debate if the confidence delta between contradictory claims is < threshold
        self.confidence_threshold = confidence_threshold

    def should_trigger_debate(
        self, rel_a: ScientificRelationship, rel_b: ScientificRelationship
    ) -> bool:
        conf_a = rel_a.provenance.confidence_score
        conf_b = rel_b.provenance.confidence_score

        # If both sides of the contradiction have strong, roughly equal evidence, trigger debate
        return abs(conf_a - conf_b) <= self.confidence_threshold
