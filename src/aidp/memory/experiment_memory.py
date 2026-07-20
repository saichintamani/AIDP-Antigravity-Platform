import json
import os
import time
from typing import Any


class ExperimentMemoryManager:
    """
    Stores the structural design (variables, controls) of VERIFIED experiments.
    """
    
    def __init__(self, storage_dir: str = ".aidp_memory") -> None:
        self.storage_dir = storage_dir
        self.experiment_file = os.path.join(self.storage_dir, "experiments.jsonl")
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def log_experiment(self, session_id: str, domain: str, experiment_design: dict[str, Any]) -> None:
        """
        Logs a VERIFIED experimental design.
        """
        entry = {
            "timestamp": time.time(),
            "session_id": session_id,
            "domain": domain,
            "experiment_design": experiment_design
        }
        
        with open(self.experiment_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    def get_experiments(self, domain: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        """
        Retrieves the top N most recent successful experiments, optionally filtered by domain.
        """
        if not os.path.exists(self.experiment_file):
            return []
            
        experiments = []
        with open(self.experiment_file) as f:
            for line in f:
                if not line.strip():
                    continue
                e_doc = json.loads(line)
                if domain is None or e_doc.get("domain") == domain:
                    experiments.append(e_doc)
                    
        # Sort by timestamp descending
        experiments.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return experiments[:limit]
