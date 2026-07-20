from aidp.retrieval.scoring import EpistemicScorer


def test_epistemic_scorer():
    scorer = EpistemicScorer()
    
    # 1. Test retracted paper rejection
    retracted_score = scorer.score_document(
        pmid="1001", 
        title="Some great discovery",
        year=2025
    )
    assert retracted_score.is_retracted
    assert retracted_score.score == 0.0
    assert "FATAL" in retracted_score.penalties_applied[0]
    
    # 2. Test keyword retraction
    keyword_score = scorer.score_document(
        pmid="9999",
        title="RETRACTED: Bad science here",
        year=2025
    )
    assert keyword_score.is_retracted
    assert keyword_score.score == 0.0
    
    # 3. Test age penalty
    old_score = scorer.score_document(
        pmid="4000",
        title="Old study",
        year=1990
    )
    # It should have a penalty and not be retracted
    assert not old_score.is_retracted
    assert any("Age penalty" in p for p in old_score.penalties_applied)

if __name__ == "__main__":
    test_epistemic_scorer()
    print("Compartment 1D Epistemic Scoring tests passed.")
