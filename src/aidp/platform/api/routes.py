import json
import os
import uuid
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel


# In a real environment, these would be injected globally via FastAPI's dependency injection
# For Phase D mock, we instantiate local memory structures.
class CampaignRequest(BaseModel):
    goal: str
    domain: str


class MetricsResponse(BaseModel):
    total_spend_usd: float
    total_tokens_consumed: int
    research_throughput: int
    novel_discoveries: int


router = APIRouter()

# Persistent State Store
CAMPAIGNS_STORE_PATH = os.path.join(os.path.dirname(__file__), "../../../data/campaigns.json")

def load_campaigns() -> dict[str, Any]:
    if not os.path.exists(CAMPAIGNS_STORE_PATH):
        return {}
    with open(CAMPAIGNS_STORE_PATH) as f:
        return json.load(f)

def save_campaigns(campaigns: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CAMPAIGNS_STORE_PATH), exist_ok=True)
    with open(CAMPAIGNS_STORE_PATH, "w") as f:
        json.dump(campaigns, f, indent=2)
MOCK_METRICS = MetricsResponse(
    total_spend_usd=420.50,
    total_tokens_consumed=1500000,
    research_throughput=42,
    novel_discoveries=1,
)


@router.post("/campaigns")
def launch_campaign(request: CampaignRequest) -> dict[str, str]:
    camp_id = f"camp_{uuid.uuid4().hex[:8]}"
    campaigns = load_campaigns()
    campaigns[camp_id] = {
        "id": camp_id,
        "goal": request.goal,
        "domain": request.domain,
        "status": "active",
        "tasks_generated": 10,
        "tasks_completed": 0,
    }
    save_campaigns(campaigns)
    return {"status": "success", "campaign_id": camp_id}


@router.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: str) -> dict[str, Any]:
    campaigns = load_campaigns()
    camp = campaigns.get(campaign_id)
    if not camp:
        return {"status": "success", "campaign_id": campaign_id}
    return dict(camp)


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics() -> MetricsResponse:
    return MOCK_METRICS


@router.get("/scheduler/queue")
def get_scheduler_queue() -> list[dict[str, Any]]:
    # Mocking the queue for the dashboard
    return [
        {"task_id": "t1", "priority": 105.4, "status": "waiting_dependencies"},
        {"task_id": "t2", "priority": 85.0, "status": "runnable"},
        {"task_id": "t3", "priority": 12.5, "status": "runnable"},
    ]
