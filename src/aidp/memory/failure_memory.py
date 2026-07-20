import json
import os
import time
from typing import Any


class FailureMemoryManager:
    """
    Logs catastrophic failures or rejected hypotheses to prevent the system from repeating flaws.
    Upgraded to act as an Anti-Gravity Memory module.
    """
    
    def __init__(self, storage_dir: str = ".aidp_memory") -> None:
        self.storage_dir = storage_dir
        self.failure_file = os.path.join(self.storage_dir, "failures.jsonl")
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def log_failure(self, session_id: str, failure_type: str, domain: str, context: dict[str, Any], critique: str) -> None:
        """
        Logs a failure event (e.g. hypothesis rejected by DebateEngine or FormalVerificationEngine).
        """
        entry = {
            "timestamp": time.time(),
            "session_id": session_id,
            "failure_type": failure_type,
            "domain": domain,
            "context": context,
            "critique": critique
        }
        
        with open(self.failure_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    def get_failures(self, domain: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        """
        Retrieves the top N most recent failures, optionally filtered by domain.
        """
        if not os.path.exists(self.failure_file):
            return []
            
        failures = []
        with open(self.failure_file) as f:
            for line in f:
                if not line.strip():
                    continue
                f_doc = json.loads(line)
                if domain is None or f_doc.get("domain") == domain:
                    failures.append(f_doc)
                    
        # Sort by timestamp descending
        failures.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return failures[:limit]
