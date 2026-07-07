from aidp.explainability.uncertainty import UncertaintyEngine


def test_uncertainty_engine() -> None:
    """Validates multidimensional uncertainty vector calculations."""
    engine = UncertaintyEngine()

    retrieval_scores = [0.9, 0.85, 0.88]
    model_confidence = 0.95

    unc = engine.estimate_uncertainty(retrieval_scores, model_confidence)

    # Assert model uncertainty is 1.0 - confidence
    assert abs(unc.model - 0.05) < 1e-5

    # Assert retrieval uncertainty is 1.0 - mean(scores)
    mean_ret = sum(retrieval_scores) / len(retrieval_scores)
    assert abs(unc.retrieval - (1.0 - mean_ret)) < 1e-5

    # Assert total uncertainty is a blended float
    total = unc.total_uncertainty
    assert 0.0 <= total <= 1.0
