import os
import sys
import time

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.core.orchestration.sync_loop import SyncLoop
from aidp.knowledge.evolution.belief_revision import BeliefReviser
from aidp.knowledge.evolution.conflict_resolution import ContradictionDetector
from aidp.knowledge.world_model import WorldModel


@pytest.mark.asyncio
async def test_massively_parallel_discovery_sessions():
    """
    Load test: Verifies that SyncLoop can handle 50 simultaneous discovery sessions 
    asynchronously without deadlocking or failing.
    """
    
    # Initialize core modules
    world_model = WorldModel()
    belief_reviser = BeliefReviser()
    detector = ContradictionDetector()
    
    sync_loop = SyncLoop(
        world_model=world_model,
        belief_reviser=belief_reviser,
        detector=detector
    )
    
    # Mock network connectors so we don't block the event loop or hit rate limits
    class MockProvenance:
        def __init__(self, query):
            self.claim_text = query
            self.confidence_score = 0.5

    class MockConnector:
        def fetch_literature_provenance(self, query):
            return [MockProvenance(query)]
            
    sync_loop.pubmed = MockConnector()
    sync_loop.arxiv = MockConnector()

    
    # We will generate 50 mock queries
    queries = [f"Target protein {i}" for i in range(50)]
    
    # Measure execution time
    start_time = time.time()
    
    # Execute batch in parallel
    results = await sync_loop.run_parallel_batch(queries)
    
    end_time = time.time()
    
    # Verify all 50 completed successfully
    assert len(results) == 50
    for res in results:
        assert isinstance(res, dict)
        assert "hypotheses" in res
        
    # Since each async session has `await asyncio.sleep(0.1)` * 2 = 0.2s of simulated IO
    # Running 50 synchronously would take ~10 seconds. 
    # Running asynchronously should take < 1.0 second.
    assert (end_time - start_time) < 2.0
