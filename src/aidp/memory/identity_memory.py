import json
import os
from typing import Any


class IdentityMemoryManager:
    """
    Manages the core philosophical directives and operational parameters of AIDP.
    Ensures the agent always knows *what* it is and *why* it operates as it does.
    """
    
    def __init__(self, storage_dir: str = ".aidp_memory") -> None:
        self.storage_dir = storage_dir
        self.identity_file = os.path.join(self.storage_dir, "identity.json")
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        if not os.path.exists(self.identity_file):
            # Default initialization based on current directive
            default_identity = {
                "core_directive": "We are optimizing epistemic reliability.",
                "operational_parameters": [
                    "Every architectural proposal must answer what uncertainty it reduces.",
                    "Every architectural proposal must answer how reduction is measured.",
                    "Every architectural proposal must state what evidence proves it wrong.",
                    "Every architectural proposal must state what regression signature appears if removed.",
                    "Every architectural proposal must be understood by future investigators."
                ],
                "version": "v1.0.0"
            }
            with open(self.identity_file, "w") as f:
                json.dump(default_identity, f, indent=4)

    def get_identity(self) -> dict[str, Any]:
        with open(self.identity_file) as f:
            return json.load(f)

    def update_directive(self, new_directive: str) -> None:
        identity = self.get_identity()
        identity["core_directive"] = new_directive
        with open(self.identity_file, "w") as f:
            json.dump(identity, f, indent=4)
