from aidp.evaluation.suite import ScientificEvaluationSuite


def test_evaluation_suite() -> None:
    suite = ScientificEvaluationSuite()

    # Run multiple mocked campaigns
    suite.evaluate_campaign_mock("Oncology")
    suite.evaluate_campaign_mock("Materials")

    metrics = suite.aggregate_metrics()

    # Assert all keys are present
    assert "discovery_quality_novelty" in metrics
    assert "discovery_quality_validity" in metrics
    assert "evidence_quality_score" in metrics
    assert "calibration_error" in metrics
    assert "cost_efficiency_eig_per_usd" in metrics
    assert "reproducibility_variance" in metrics

    # Assert values are calculated correctly (averages)
    assert metrics["discovery_quality_novelty"] == (0.85 + 0.75) / 2
