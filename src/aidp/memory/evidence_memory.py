import json
import os
import time


class EvidenceMemoryManager:
    """
    Stores EpistemicEvidence that was used in highly confident, verified protocols.
    Allows the platform to reuse strong evidence across different sessions.
    """
    
    def __init__(self, storage_dir: str = ".aidp_memory") -> None:
        self.storage_dir = storage_dir
        self.evidence_file = os.path.join(self.storage_dir, "evidence.jsonl")
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def log_evidence(self, session_id: str, claim_id: str, evidence_list: list[dict]) -> None:
        """
        Logs a list of EpistemicEvidence objects (as dicts).
        """
        for ev in evidence_list:
            entry = {
                "timestamp": time.time(),
                "session_id": session_id,
                "claim_id": claim_id,
                "evidence": ev
            }
            with open(self.evidence_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
            
    def get_evidence(self, limit: int = 10) -> list[dict]:
        """
        Retrieves the most recent verified evidence.
        """
        if not os.path.exists(self.evidence_file):
            return []
            
        evidence = []
        with open(self.evidence_file) as f:
            for line in f:
                if not line.strip():
                    continue
                evidence.append(json.loads(line))
                    
        # Sort by timestamp descending
        evidence.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return evidence[:limit]
