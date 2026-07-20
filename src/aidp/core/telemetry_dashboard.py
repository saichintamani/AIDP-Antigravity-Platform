import json

from aidp.intelligence.epistemic_models import EpistemicLedger


class TelemetryExporter:
    """
    Exports the Epistemic Ledger and Confidence Lineage into structured formats 
    (JSON/CSV) for external visualization tools (e.g. Grafana).
    """
    
    @staticmethod
    def export_ledger_to_json(ledger: EpistemicLedger, filepath: str = "ledger_telemetry.json") -> str:
        """
        Exports the entire ledger state to JSON.
        """
        export_data = []
        for claim in ledger.get_all_claims():
            claim_data = {
                "claim_id": claim.claim_id,
                "text": claim.claim_text,
                "overall_confidence": claim.confidence.overall_confidence,
                "status": claim.verification_status.name,
                "lineage": [
                    {
                        "event_id": event.event_id,
                        "timestamp": event.timestamp,
                        "dimension": event.dimension,
                        "delta": event.delta,
                        "reason": event.reason
                    }
                    for event in claim.confidence.lineage
                ]
            }
            export_data.append(claim_data)
            
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        return filepath
        
    @staticmethod
    def export_lineage_to_csv(ledger: EpistemicLedger, filepath: str = "lineage_telemetry.csv") -> str:
        """
        Exports just the lineage deltas to CSV for time-series visualization.
        """
        import csv
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['claim_id', 'event_id', 'timestamp', 'dimension', 'delta', 'reason']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for claim in ledger.get_all_claims():
                for event in claim.confidence.lineage:
                    writer.writerow({
                        'claim_id': claim.claim_id,
                        'event_id': event.event_id,
                        'timestamp': event.timestamp,
                        'dimension': event.dimension,
                        'delta': event.delta,
                        'reason': event.reason
                    })
                    
        return filepath
