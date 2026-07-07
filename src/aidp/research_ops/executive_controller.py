from aidp.research_ops.budget_controller import BudgetController
from aidp.research_ops.campaign_manager import CampaignManager
from aidp.research_ops.laboratory_metrics import KPIDashboard


class ExecutiveController:
    """
    The highest-level control loop. Monitors KPIs and Campaigns, and makes
    executive decisions to pause, terminate, or re-allocate resources.
    """

    def __init__(
        self, campaign_manager: CampaignManager, dashboard: KPIDashboard, budget: BudgetController
    ):
        self.campaign_manager = campaign_manager
        self.dashboard = dashboard
        self.budget = budget

    def evaluate_laboratory_health(self) -> None:
        """
        Runs periodically to ensure the lab is operating efficiently.
        """
        metrics = self.dashboard.get_snapshot()

        # Example Policy: If cost per discovery exceeds $500, pause expensive campaigns
        if metrics.novel_discoveries > 0 and metrics.cost_per_discovery > 500.0:
            # We would normally signal the budget controller or scheduler
            # For Phase C, we just print/log the intervention
            pass

        # Example Policy: If a campaign has generated 100 tasks but 0 completed, flag for review
        for camp in self.campaign_manager.active_campaigns:
            if camp.tasks_generated > 100 and camp.tasks_completed == 0:
                camp.status = "paused_for_executive_review"
