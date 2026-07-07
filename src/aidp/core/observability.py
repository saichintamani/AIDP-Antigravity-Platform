import time
from typing import Any, Optional
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()


class TelemetryManager:
    """
    Handles structured logging, execution traces, and metrics (latency, token cost).
    """

    def __init__(self) -> None:
        self.metrics: dict[str, Any] = {
            "total_cost_usd": 0.0,
            "total_api_calls": 0,
            "traces": []
        }
        self.campaign_start_time: Optional[float] = None

    def start_campaign(self, campaign_id: str) -> None:
        self.campaign_start_time = time.time()
        logger.info("campaign_started", campaign_id=campaign_id)

    def log_api_call(self, provider: str, cost: float, latency_sec: float, success: bool, error: Optional[str] = None) -> None:
        self.metrics["total_cost_usd"] += cost
        self.metrics["total_api_calls"] += 1
        
        trace_data = {
            "provider": provider,
            "cost": cost,
            "latency": latency_sec,
            "success": success
        }
        if error:
            trace_data["error"] = error
            
        self.metrics["traces"].append(trace_data)
        logger.info("api_call", **trace_data)

    def end_campaign(self, campaign_id: str) -> dict[str, Any]:
        duration = 0.0
        if self.campaign_start_time:
            duration = time.time() - self.campaign_start_time
            
        summary = {
            "campaign_id": campaign_id,
            "duration_sec": duration,
            "total_cost_usd": self.metrics["total_cost_usd"],
            "total_api_calls": self.metrics["total_api_calls"]
        }
        logger.info("campaign_ended", **summary)
        return self.metrics
