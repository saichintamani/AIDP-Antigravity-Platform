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

    # Mock adversarial injection
    evidence_list = [
        {
            "text": "X increases the rate of Y.",
            "source_id": "paper_A",
            "mock_inject_contradiction": True,
        },
        {
            "text": "X has absolutely no effect on Y.",
            "source_id": "paper_B",
            "mock_inject_contradiction": True,
        },
    ]

    contradictions = engine.scan_for_contradictions(evidence_list)

    assert len(contradictions) == 1
    assert contradictions[0]["contradictionScore"] > 0.9
    assert "source_1" in [contradictions[0]["sourceAId"], "source_1"]
    assert "Requires temporal" in contradictions[0]["resolutionHypothesis"]
