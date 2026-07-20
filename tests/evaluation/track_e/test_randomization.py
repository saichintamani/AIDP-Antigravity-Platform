from fastapi.testclient import TestClient

from aidp.evaluation.track_e_server import app
from tests.evaluation.datasets.historical_cases import ALL_CASES

client = TestClient(app)

def test_randomization_audit():
    """
    Audits the /api/cases endpoint to ensure that:
    1. The experiment order is statistically randomized across sessions.
    2. No leakage metadata (like "is_winner") is transmitted.
    3. The internal strings match the original candidates without corruption.
    """
    # Fetch 10 times to check for different orderings
    responses = []
    for _ in range(10):
        response = client.get("/api/cases")
        assert response.status_code == 200
        responses.append(response.json()["cases"])
    
    # Check HRC_PRIONS specifically (or the first case)
    prions_candidates_list = []
    for r in responses:
        prions_case = next(c for c in r if c["case_id"] == "HRC_PRIONS")
        
        # Audit leakage
        assert "historical_winner" not in prions_case
        assert "aidp_rank" not in prions_case
        assert "status" not in prions_case
        
        # Verify content hasn't been corrupted
        original_prions_case = next(c for c in ALL_CASES if c.case_id == "HRC_PRIONS")
        original_candidates = set(original_prions_case.candidate_experiments)
        
        served_candidates = prions_case["candidates"]
        assert len(served_candidates) == len(original_candidates)
        assert set(served_candidates) == original_candidates
        
        prions_candidates_list.append(tuple(served_candidates))
        
    # Verify that the order is not identical across 10 requests (highly improbable if truly random)
    unique_orderings = set(prions_candidates_list)
    assert len(unique_orderings) > 1, "The experiments were served in the exact same order 10 times. Randomization is broken."
    
    print(f"Randomization Audit Passed. Found {len(unique_orderings)} unique orderings across 10 requests.")

if __name__ == "__main__":
    test_randomization_audit()
