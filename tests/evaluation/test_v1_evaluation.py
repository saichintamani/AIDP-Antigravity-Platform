from aidp.evaluation.framework import ScientificReportCard
from aidp.evaluation.gold_standard_runner import GoldStandardRunner


def test_framework_report_card() -> None:
    card = ScientificReportCard()
    report = card.generate_report_card({"domain": "Oncology"})

    assert "scientific_correctness" in report
    assert "hallucination_rate" in report
    assert "expected_information_gain" in report


def test_gold_standard_runner() -> None:
    # Use the benchmark json created in the repo
    runner = GoldStandardRunner("data/benchmarks/gold_standard.json")
    result = runner.run_benchmark("crispr_cas9")

    assert result["case_id"] == "crispr_cas9"
    assert "predicted_discovery" in result
    assert not result["historical_leakage_detected"]
