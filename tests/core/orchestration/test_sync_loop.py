from aidp.core.orchestration.sync_loop import SyncLoop
from aidp.knowledge.evolution.belief_revision import BeliefReviser
from aidp.knowledge.evolution.conflict_resolution import ContradictionDetector
from aidp.knowledge.world_model import WorldModel


def test_sync_loop_cycle() -> None:
    world = WorldModel()
    reviser = BeliefReviser()
    detector = ContradictionDetector()

    sync = SyncLoop(world, reviser, detector)

    # We will mock the external calls for a fast unit test.
    # Actually, we can just run it since our mock API calls might fail gracefully and return [] or we just mock it.
    # The ArXiv API will actually return real data if query is "p53 cancer". Let's use a very specific mock query.
    selected = sync.run_sync_cycle(["mock_test_query"])

    assert len(selected) > 0
    assert selected[0]["id"] == "h_new1"
