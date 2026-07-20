import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.knowledge.external.clinicaltrials_client import ClinicalTrialsClient
from aidp.knowledge.external.pubmed_client import PubMedClient


@pytest.mark.integration
def test_pubmed_client_fetches_real_data():
    """
    Integration test: Hits the real PubMed API to retrieve abstracts.
    Requires internet connection.
    """
    client = PubMedClient()
    results = client.search_abstracts("crispr cas9 cancer", max_results=2)
    
    # We should get up to 2 results back
    assert len(results) > 0
    
    # Each result should have a pmid, title, and abstract
    assert "pmid" in results[0]
    assert "abstract" in results[0]
    assert results[0]["source"] == "PubMed"

@pytest.mark.integration
def test_clinicaltrials_client_fetches_real_data():
    """
    Integration test: Hits the real ClinicalTrials.gov API to retrieve protocols.
    Requires internet connection.
    """
    client = ClinicalTrialsClient()
    results = client.search_trials("diabetes", max_results=2)
    
    # We should get up to 2 results back
    assert len(results) > 0
    
    # Each result should have nct_id and methodology data
    assert "nct_id" in results[0]
    assert "phases" in results[0]
    assert results[0]["source"] == "ClinicalTrials.gov"
