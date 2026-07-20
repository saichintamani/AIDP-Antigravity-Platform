from aidp.discovery.contradiction import ContradictionDetectionEngine
from aidp.discovery.gap import KnowledgeGapEngine


def test_knowledge_gap_detection() -> None:
    """Validates that missing edges with high entropy are surfaced."""
    engine = KnowledgeGapEngine()

    # Mock evidence graph with two unconnected nodes
    evidence_graph = {
        "nodes": [{"id": "node-1", "label": "Protein X"}, {"id": "node-2", "label": "Disease Y"}],
        "edges": [],
    }

    gaps = engine.detect_gaps(evidence_graph)

    assert len(gaps) == 1
    assert gaps[0]["conceptA"] == "Protein X"
    assert gaps[0]["conceptB"] == "Disease Y"
    assert gaps[0]["estimatedEntropy"] > 0.8
    assert gaps[0]["confidenceMissing"] > 0.9


def test_contradiction_detection() -> None:
    """Validates semantic collision surfacing between two claims."""
    engine = ContradictionDetectionEngine()

    class MockRelation:
        def __init__(self, s, t):
            self.source_entity_id = s
            self.target_entity_id = t
            self.relation_type = "affects"
            self.provenance = None
            
    class MockWorldModel:
        def __init__(self):
            self.entities = {}
        def find_contradictions(self):
            return [(MockRelation("X", "Y"), MockRelation("X", "Y"))]
            
    contradictions = engine.scan_for_contradictions(MockWorldModel())

    assert len(contradictions) == 1
    assert contradictions[0]["contradictionScore"] > 0.9
    assert "Requires temporal" in contradictions[0]["resolutionHypothesis"]
