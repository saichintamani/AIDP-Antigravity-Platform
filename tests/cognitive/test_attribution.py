from aidp.explainability.attribution import AttributionEngine
from aidp.explainability.counterfactual import CounterfactualAnalyzer


def test_attribution_engine() -> None:
    """Validates that a raw retrieval result generates explicit feature attributions."""
    engine = AttributionEngine()

    mock_bytes = b"mock_cognitive_object"

    result = engine.attribute_retrieval(
        cognitive_object_bytes=mock_bytes,
        rank=1,
        raw_similarity_score=0.85,
        query="Explain attribution",
    )

    assert result.rank == 1
    assert result.cognitive_object_bytes == mock_bytes
    assert "0.85" in result.reason_retrieved
    assert result.feature_attribution.vector_similarity == 0.85
    assert result.feature_attribution.keyword_contribution == 0.425
    assert result.feature_attribution.confidence > 0.8


def test_counterfactual_analyzer() -> None:
    """Validates counterfactual dependency checks."""
    analyzer = CounterfactualAnalyzer()

    # 1. Hypothesis depends on evidence
    evidence = [{"text": "Sky is blue."}]
    hypothesis = "The sky is blue."

    assert analyzer.check_dependency(hypothesis, evidence, hypothesis)

    # 2. Hallucination without evidence
    assert not analyzer.check_dependency(hypothesis, [], hypothesis)
