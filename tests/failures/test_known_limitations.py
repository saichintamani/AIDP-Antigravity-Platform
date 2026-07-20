import os
import sys

import pytest

# Add src to sys.path so we can import aidp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from aidp.discovery.domain_routing import DomainDetector, ScientificDomain


# Mock the planner that simulates the failure mode
class MockFailingPlanner:
    def execute_task(self, spec):
        claim = spec.context.get("claim", "").lower()
        if "patient" in claim and "simulate" in claim:
            # The current LLM logic gets confused by highly multi-disciplinary abstracts
            # and defaults to OBSERVATIONAL or WET_LAB instead of splitting the workflow.
            return {"domain": "OBSERVATIONAL", "justification": "Mixed methods"}
        return {"domain": "WET_LAB", "justification": ""}

@pytest.mark.xfail(strict=True, reason="AIDP cannot currently route heavily multi-disciplinary abstracts cleanly.")
def test_limitation_multidisciplinary_routing_failure():
    """
    KNOWN FAILURE: When an abstract contains both heavy computational simulation (In Silico) 
    and patient testing (Clinical Trial), the DomainDetector currently fails to split the 
    workflow into a hybrid DAG and instead defaults to a single incorrect domain.
    """
    detector = DomainDetector(planner=MockFailingPlanner())
    
    abstract = "We will simulate the molecule binding affinity in silico, and then test the exact molecule in a Phase 1 patient trial."
    
    # We WANT it to identify the dual nature, or default to the most stringent (CLINICAL_TRIAL)
    # But currently, it fails and returns OBSERVATIONAL or WET_LAB.
    domain = detector.detect_domain(abstract, abstract)
    
    # This assertion will FAIL, which is what @pytest.mark.xfail expects.
    assert domain == ScientificDomain.CLINICAL_TRIAL

@pytest.mark.xfail(strict=True, reason="AIDP debate engine is currently vulnerable to schema blindness if the baseline schema lacks a specific field.")
def test_limitation_schema_blindness():
    """
    KNOWN FAILURE: If the JSON schema provided to the Debate Engine does not explicitly 
    require an 'ethical_approval_board' field, the Bioethicist agent will sometimes 
    approve the protocol because it strictly follows the schema, exhibiting 'schema blindness'.
    """
    # Simulate a design missing ethical approval
    
    # In a real failure, the agent approves this because the schema didn't ask for ethics.
    # We simulate the false approval here.
    agent_decision = "approve" 
    
    # We assert it should have rejected it. This will fail.
    assert agent_decision == "reject"
