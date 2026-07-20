import json
import os
import time
from typing import Any


class DecisionMemoryManager:
    """
    Logs branching choices made by the workflow to ensure structural decisions are auditable.
    Upgraded to include Confidence Calibration breakdowns.
    """
    
    def __init__(self, storage_dir: str = ".aidp_memory") -> None:
        self.storage_dir = storage_dir
        self.decision_file = os.path.join(self.storage_dir, "decisions.jsonl")
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def log_decision(self, session_id: str, context: str, decision: str, rationale: str, confidence_breakdown: dict[str, Any] | None = None) -> None:
        """
        Logs a decision along with its rationale and confidence breakdown.
        """
        entry = {
            "timestamp": time.time(),
            "session_id": session_id,
            "context": context,
            "decision": decision,
            "rationale": rationale,
            "confidence_breakdown": confidence_breakdown or {}
        }
        
        with open(self.decision_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    def get_decisions(self, session_id: str | None = None) -> list[dict[str, Any]]:
        if not os.path.exists(self.decision_file):
            return []
            
        decisions = []
        with open(self.decision_file) as f:
            for line in f:
                if not line.strip():
                    continue
                d = json.loads(line)
                if session_id is None or d.get("session_id") == session_id:
                    decisions.append(d)
        return decisions
