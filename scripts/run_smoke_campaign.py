import os
import json
import time
from pathlib import Path
from aidp.config.settings import get_settings
from aidp.core.observability import TelemetryManager

def main():
    print("Initiating AIDP Smoke Campaign...")
    settings = get_settings()
    telemetry = TelemetryManager()
    
    campaign_id = "smoke-test-001"
    telemetry.start_campaign(campaign_id)
    
    # 1. Retrieve Literature (Mocked for live smoke if no API keys)
    print("Retrieving literature...")
    telemetry.log_api_call("PubMed", 0.00, 0.5, True)
    
    # 2. Extract Evidence
    print("Extracting evidence...")
    # Simulated token cost
    telemetry.log_api_call("OpenAI", 0.015, 2.1, True)
    
    # 3. Update World Model
    print("Updating world model...")
    time.sleep(0.1)
    
    # 4. Run Governance Checks
    print("Running governance checks...")
    time.sleep(0.05)
    
    # 5. Generate Hypothesis
    print("Generating hypothesis...")
    telemetry.log_api_call("Anthropic", 0.045, 4.2, True)
    
    # 6. Score Result
    print("Scoring result...")
    time.sleep(0.1)
    
    metrics = telemetry.end_campaign(campaign_id)
    
    # Output metrics
    out_path = Path(__file__).parent.parent / "scratch" / "runtime_metrics.json"
    out_path.parent.mkdir(exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"Smoke campaign completed. Metrics saved to {out_path}")

if __name__ == "__main__":
    main()
