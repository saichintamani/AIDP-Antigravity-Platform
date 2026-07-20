from enum import StrEnum
from typing import Any


class PlanningDomain(StrEnum):
    WET_LAB_ASSAY = "WET_LAB_ASSAY"
    CLINICAL_TRIAL = "CLINICAL_TRIAL"
    COMPUTATIONAL_SCREENING = "COMPUTATIONAL_SCREENING"

class DomainRouter:
    """
    Analyzes the discovery context and query to determine the appropriate 
    scientific domain for protocol synthesis.
    """
    def __init__(self):
        # Keyword-based heuristics for MVP domain routing
        self.clinical_keywords = {"patient", "cohort", "phase", "trial", "human", "placebo", "survival"}
        self.computational_keywords = {"docking", "simulation", "molecular dynamics", "in silico", "alphafold", "prediction"}
        self.wet_lab_keywords = {"in vitro", "cell line", "assay", "western blot", "crispr", "knockout", "mouse", "in vivo"}

    def route(self, question: str, knowledge_context: dict[str, Any]) -> PlanningDomain:
        """
        Determine the planning domain based on the question and extracted entities.
        """
        question_lower = question.lower()
        
        # 1. Check for clinical intent
        if any(kw in question_lower for kw in self.clinical_keywords):
            return PlanningDomain.CLINICAL_TRIAL
            
        # 2. Check for computational intent
        if any(kw in question_lower for kw in self.computational_keywords):
            return PlanningDomain.COMPUTATIONAL_SCREENING
            
        # 3. Check for wet lab intent
        if any(kw in question_lower for kw in self.wet_lab_keywords):
            return PlanningDomain.WET_LAB_ASSAY
            
        # 4. Fallback based on knowledge context entities
        if knowledge_context and "documents" in knowledge_context:
            for doc in knowledge_context.get("documents", []):
                entities = doc.get("normalized_entities", [])
                for entity in entities:
                    ent_lower = entity.lower()
                    if any(kw in ent_lower for kw in self.clinical_keywords):
                        return PlanningDomain.CLINICAL_TRIAL
                    if any(kw in ent_lower for kw in self.computational_keywords):
                        return PlanningDomain.COMPUTATIONAL_SCREENING
        
        # Default fallback
        return PlanningDomain.WET_LAB_ASSAY
