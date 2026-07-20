import os
import sys

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from aidp.discovery.domain_routing import DomainDetector, ScientificDomain


class MockPlannerForRouting:
    def __init__(self, expected_domain):
        self.expected_domain = expected_domain
        
    def execute_task(self, spec):
        claim = spec.context.get("claim", "")
        if "patient" in claim.lower() or "clinical" in claim.lower():
            return {"domain": "CLINICAL_TRIAL", "justification": "Mock justification"}
        elif "simulate" in claim.lower() or "in silico" in claim.lower():
            return {"domain": "COMPUTATIONAL", "justification": "Mock justification"}
        else:
            return {"domain": "WET_LAB", "justification": "Mock justification"}

def test_routing_clinical_trial():
    detector = DomainDetector(planner=MockPlannerForRouting("CLINICAL_TRIAL"))
    domain = detector.detect_domain("Can we test this new drug in a patient cohort?", "Can we test this new drug in a patient cohort?")
    assert domain == ScientificDomain.CLINICAL_TRIAL

def test_routing_computational():
    detector = DomainDetector(planner=MockPlannerForRouting("COMPUTATIONAL"))
    domain = detector.detect_domain("Can we simulate the binding affinity in silico?", "Can we simulate the binding affinity in silico?")
    assert domain == ScientificDomain.COMPUTATIONAL

def test_routing_wet_lab():
    detector = DomainDetector(planner=MockPlannerForRouting("WET_LAB"))
    domain = detector.detect_domain("Can we assay the cells in vitro?", "Can we assay the cells in vitro?")
    assert domain == ScientificDomain.WET_LAB
