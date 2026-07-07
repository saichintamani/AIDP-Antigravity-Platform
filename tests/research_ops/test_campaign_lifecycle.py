from aidp.research_ops.campaign_manager import CampaignManager
from aidp.research_ops.economics_engine import ScientificTaskProposal
from aidp.research_ops.scheduler import IntelligentScheduler


def test_campaign_lifecycle() -> None:
    scheduler = IntelligentScheduler()
    manager = CampaignManager(scheduler)

    camp = manager.launch_campaign("Cure X", "Medicine")
    assert camp.status == "active"

    task = ScientificTaskProposal("T1", "Exp", 1, 1, 1, 1, 1, 0.1)
    manager.inject_task(camp.id, task, priority=50.0)

    assert camp.tasks_generated == 1
    assert camp.tasks_completed == 0

    # Simulate execution
    scheduler.get_next_runnable_task()
    manager.mark_task_complete(camp.id)

    assert camp.tasks_completed == 1
    assert camp.status == "completed"
