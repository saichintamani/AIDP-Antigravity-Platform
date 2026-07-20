import uuid
from dataclasses import dataclass, field

from aidp.research_ops.economics_engine import ScientificTaskProposal
from aidp.research_ops.scheduler import IntelligentScheduler


@dataclass
class ResearchCampaign:
    goal: str
    domain: str
    id: str = field(default_factory=lambda: f"camp_{uuid.uuid4()}")
    status: str = "active"
    tasks_generated: int = 0
    tasks_completed: int = 0


class CampaignManager:
    """
    Orchestrates massive hierarchies of hypotheses and experiments over weeks.
    Replaces isolated task logic.
    """

    def __init__(self, scheduler: IntelligentScheduler) -> None:
        self.scheduler = scheduler
        self.active_campaigns: list[ResearchCampaign] = []

    def launch_campaign(self, goal: str, domain: str) -> ResearchCampaign:
        camp = ResearchCampaign(goal=goal, domain=domain)
        self.active_campaigns.append(camp)
        return camp

    def inject_task(
        self,
        campaign_id: str,
        task: ScientificTaskProposal,
        priority: float,
        depends_on: list[str] | None = None,
    ) -> None:
        """Adds a task to a campaign, pushing it to the global scheduler."""
        # Find campaign
        camp = next((c for c in self.active_campaigns if c.id == campaign_id), None)
        if not camp:
            raise ValueError(f"Unknown campaign: {campaign_id}")

        camp.tasks_generated += 1
        self.scheduler.enqueue(task, priority, depends_on)

    def mark_task_complete(self, campaign_id: str) -> None:
        camp = next((c for c in self.active_campaigns if c.id == campaign_id), None)
        if camp:
            camp.tasks_completed += 1
            if camp.tasks_completed >= camp.tasks_generated:
                camp.status = "completed"
