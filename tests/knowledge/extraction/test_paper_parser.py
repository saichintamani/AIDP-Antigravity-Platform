from aidp.knowledge.extraction.paper_parser import PaperParser


def test_paper_parser() -> None:
    parser = PaperParser()
    text = "We show that CRISPR-Cas9 inhibition of p53 leads to increased apoptosis in vitro (p < 0.05). A limitation is the small sample size."

    parsed = parser.parse_paper(text)

    assert "entities" in parsed
    assert len(parsed["entities"]) > 0

    assert "methods" in parsed
    assert "CRISPR-Cas9" in str(parsed["methods"])

    assert "results" in parsed
    assert "limitations" in parsed
