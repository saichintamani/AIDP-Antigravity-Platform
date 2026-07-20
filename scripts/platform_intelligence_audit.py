import datetime
import json
import os
import sys

# Add src to sys.path so we can import aidp


from aidp.discovery.workflow import AutonomousDiscoveryOrchestrator
from aidp.platform.epistemic_logger import EpistemicLedger


def run_audit():
    print("==================================================")
    print("   AIDP PLATFORM INTELLIGENCE AUDIT - FLAGSHIP    ")
    print("==================================================")
    
    # 1. Initialize System
    # Here we should use a Mock or the real LLM Gateway depending on what's available
    # For a real flagship validation, we would use the actual Gateway.
    # But since we might not have API keys configured in this environment, 
    # we'll inject a deterministic test harness or run it and capture what we can.
    
    
    class MockGateway:
        def query(self, prompt, schema_hint=None, **kwargs):
            if schema_hint:
                # If schema_hint is a Pydantic model CLASS, instantiate it with defaults
                if isinstance(schema_hint, type):
                    try:
                        return schema_hint()
                    except Exception:
                        return {}
                return schema_hint
            return {"mock": "data"}

    gateway = MockGateway()

    orchestrator = AutonomousDiscoveryOrchestrator(gateway=gateway, requires_human_approval=False)
    
    # We will test a canonical question
    question = "Can we use a synthetic peptide to inhibit the aggregation of alpha-synuclein in Parkinson's disease?"
    print(f"\n[Audit Target]: {question}")
    
    session = orchestrator.run_discovery_cycle(question)
    
    print("\n--- Audit Results ---")
    print(f"Final State: {session.state}")
    
    # Generate the Audit Report
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": question,
        "final_state": str(session.state),
        "subsystems": {}
    }
    
    # 1. Knowledge Graph (Retrieval & Contradictions)
    report["subsystems"]["Knowledge Graph"] = {
        "observable_behavior": f"Extracted {len(session.contradictions)} contradictions/gaps.",
        "data": session.contradictions
    }
    
    # 2. Domain Router
    # We can infer the routed domain based on the planner that generated the claim
    ledger = EpistemicLedger()
    claims = ledger.get_all_claims()
    latest_claim = claims[-1] if claims else None
    
    if latest_claim:
        report["subsystems"]["Domain Router"] = {
            "observable_behavior": f"Routed to {latest_claim.generated_by}",
            "data": latest_claim.generated_by
        }
        
        # 3. Scientific Planning Layer (SPL)
        report["subsystems"]["Scientific Planning Layer"] = {
            "observable_behavior": f"Generated experimental design with {len(latest_claim.assumptions)} explicit assumptions.",
            "data": session.experiment_design
        }
        
        # 4. Formal Verification
        # Check telemetry for verification report
        ver_report = session.telemetry.get("verification_report", {})
        report["subsystems"]["Formal Verification"] = {
            "observable_behavior": f"Formal Verification Status: {ver_report.get('status')}",
            "data": ver_report
        }
        
        # 5. Debate Engine
        report["subsystems"]["Debate Engine"] = {
            "observable_behavior": f"Generated {len(session.debate_record.get('critiques', []))} independent adversarial critiques. Consensus Reached: {session.debate_record.get('consensusReached')}",
            "data": session.debate_record
        }
        
        # 6. Confidence Lineage
        report["subsystems"]["Confidence Lineage"] = {
            "observable_behavior": f"Tracked {len(latest_claim.confidence_lineage)} lineage events adjusting the multi-dimensional ontology.",
            "data": [vars(e) for e in latest_claim.confidence_lineage]
        }
    
    # Write report to artifacts
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PLATFORM_INTELLIGENCE_AUDIT.json"))
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"\nAudit completed. Raw data saved to {report_path}")

if __name__ == "__main__":
    run_audit()
