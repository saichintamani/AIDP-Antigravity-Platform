import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.discovery.domain_routing import DomainDetector, ScientificDomain


# For the benchmark we need to simulate the LLM's classification logic
class MockRobustPlanner:
    def execute_task(self, spec):
        claim = spec.context.get("claim", "").lower()
        if "patient" in claim or "trial" in claim:
            return {"domain": "CLINICAL_TRIAL", "justification": ""}
        elif "simulate" in claim or "docking" in claim or "in silico" in claim:
            return {"domain": "COMPUTATIONAL", "justification": ""}
        elif "repurpose" in claim or "fda" in claim:
            # We map drug repurposing to OBSERVATIONAL or CLINICAL_TRIAL based on context
            return {"domain": "OBSERVATIONAL", "justification": ""}
        elif "literature" in claim or "contradict" in claim or "synthesis" in claim:
            return {"domain": "OBSERVATIONAL", "justification": ""}
        elif "material" in claim or "alloy" in claim or "tensile" in claim:
            return {"domain": "MATERIALS", "justification": ""}
        else:
            return {"domain": "WET_LAB", "justification": ""}

def test_molecular_biology():
    detector = DomainDetector(planner=MockRobustPlanner())
    domain = detector.detect_domain("CRISPR-Cas9 knockout of gene X in HEK293 cells", "CRISPR-Cas9 knockout of gene X in HEK293 cells")
    assert domain == ScientificDomain.WET_LAB

def test_drug_repurposing():
    detector = DomainDetector(planner=MockRobustPlanner())
    domain = detector.detect_domain("FDA approved drug Y can be repurposed for disease Z", "FDA approved drug Y can be repurposed for disease Z")
    assert domain == ScientificDomain.OBSERVATIONAL

def test_literature_synthesis():
    detector = DomainDetector(planner=MockRobustPlanner())
    domain = detector.detect_domain("Meta-analysis of literature shows conflicting evidence on X", "Meta-analysis of literature shows conflicting evidence on X")
    assert domain == ScientificDomain.OBSERVATIONAL

def test_contradiction_detection():
    detector = DomainDetector(planner=MockRobustPlanner())
    domain = detector.detect_domain("Paper A contradicts Paper B regarding the mechanism", "Paper A contradicts Paper B regarding the mechanism")
    assert domain == ScientificDomain.OBSERVATIONAL

def test_experimental_design_materials():
    detector = DomainDetector(planner=MockRobustPlanner())
    domain = detector.detect_domain("Design a new alloy with high tensile strength", "Design a new alloy with high tensile strength")
    assert domain == ScientificDomain.MATERIALS
