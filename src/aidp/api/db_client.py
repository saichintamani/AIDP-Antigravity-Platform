import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseClient:
    """
    Mock integration for Firebase / Supabase backend.
    In a true cloud deployment, this connects via their respective SDKs.
    For this phase, it persists data securely to a cloud-ready JSON sink.
    """
    def __init__(self):
        self.db_path = "data/cloud_db/evaluations.json"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_evaluation_record(self, record: dict):
        logger.info("Persisting evaluation to Supabase/Firebase backend...")
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
                
            record["timestamp"] = datetime.utcnow().isoformat() + "Z"
            db.append(record)
            
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4)
                
            logger.info("Record saved successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to sync with DB: {e}")
            return False
