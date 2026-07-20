from typing import Any


class DomainMetricValidator:
    """
    Validates that a generated experiment design meets strict domain-specific
    structural requirements before hitting the FormalVerification layer.
    """
    def validate_design(self, design: dict[str, Any]) -> dict[str, Any]:
        """
        Returns a dict: {"valid": bool, "penalties": List[str]}
        """
        domain = design.get("domain", "UNKNOWN").upper()
        methodology = design
        
        penalties = []
        valid = True
        
        if domain == "WET_LAB":
            # Must have controls
            controls = methodology.get("controls", [])
            if not controls:
                penalties.append("FATAL: Wet Lab protocol missing controls.")
                valid = False
                
        elif domain == "CLINICAL_TRIAL":
            # Must have randomization and comparator
            if "comparator_arms" not in methodology:
                penalties.append("FATAL: Clinical trial missing comparator arm.")
                valid = False
            if "randomization" not in methodology:
                penalties.append("FATAL: Clinical trial missing randomization details.")
                valid = False
                
        elif domain == "COMPUTATIONAL":
            # Must have data splits
            splits = methodology.get("data_splits", {})
            if "training_set" not in splits or "validation_set" not in splits:
                penalties.append("FATAL: Computational methodology missing dataset splits.")
                valid = False
                
        else:
            penalties.append(f"WARNING: Unknown domain '{domain}' - cannot validate strict metrics.")
            
        return {
            "valid": valid,
            "penalties": penalties
        }
