

class EvidenceGraph:
    """
    Connects the exact pieces of evidence (papers, experiments) that support or contradict
    a given ScientificRelationship.
    """

    def __init__(self) -> None:
        # Maps a ScientificRelationship ID to a list of ExperimentalResult IDs
        self.supports_edges: dict[str, list[str]] = {}
        self.contradicts_edges: dict[str, list[str]] = {}

    def add_supporting_evidence(self, relationship_id: str, experiment_id: str) -> None:
        if relationship_id not in self.supports_edges:
            self.supports_edges[relationship_id] = []
        self.supports_edges[relationship_id].append(experiment_id)

    def add_contradicting_evidence(self, relationship_id: str, experiment_id: str) -> None:
        if relationship_id not in self.contradicts_edges:
            self.contradicts_edges[relationship_id] = []
        self.contradicts_edges[relationship_id].append(experiment_id)

    def calculate_evidence_quality_score(self, relationship_id: str) -> float:
        """
        Calculates a holistic Knowledge Quality Score based on replication strength.
        """
        supports = len(self.supports_edges.get(relationship_id, []))
        contradicts = len(self.contradicts_edges.get(relationship_id, []))

        if supports == 0 and contradicts == 0:
            return 0.0

        # Basic scoring: Net positive evidence normalized.
        # In a real system, this considers journal impact factor, p-values, etc.
        net = supports - contradicts
        total = supports + contradicts

        return max(0.0, net / total)
