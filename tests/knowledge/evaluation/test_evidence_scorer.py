from aidp.knowledge.evaluation.evidence_scorer import EvidenceScorer


def test_evidence_scorer() -> None:
    scorer = EvidenceScorer()

    parsed_paper = {"methods": ["CRISPR-Cas9"], "results": ["p < 0.05"]}
    raw_text = "Data availability statement: All data is available on GitHub."

    scores = scorer.score_paper(parsed_paper, raw_text)

    assert scores["methodology_quality"] == 0.8
    assert scores["reproducibility"] == 0.9
    assert scores["statistical_strength"] == 0.8
    assert scores["base_confidence"] > 0.5
