import json
import signal
import uuid
from pydantic import BaseModel, Field

from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import Claim
from aidp.intelligence.providers.factory import create_default_gateway

class GenerativeHypothesis(BaseModel):
    title: str = Field(..., description="Short title of the hypothesis")
    rationale: str = Field(..., description="Why this hypothesis resolves the core epistemic tension and aligns with all constraints")
    experimental_design: str = Field(..., description="The concrete steps to test this hypothesis in the lab")
    expected_outcome: str = Field(..., description="What the expected outcome is if the hypothesis is true")

class StrategicIntelligenceLayer:
    """
    The executive brain that autonomously generates novel hypotheses and ranks them.
    Now upgraded to a Generative Multi-Agent Discovery Engine.
    """
    
    def __init__(self, gateway=None, memory_system=None):
        self.gateway = gateway or create_default_gateway()
        self.memory_system = memory_system
        
    def _hostile_peer_review(self, hypothesis: GenerativeHypothesis, case: HistoricalReplayCase) -> bool:
        """
        Adversarial Agent: Attempts to destroy the hypothesis.
        Returns True if the hypothesis survives, False if it is rejected.
        """
        evidence_strings = [e.extracted_text if hasattr(e, "extracted_text") else str(e) for e in case.known_evidence]
        evidence_text = "\n".join(evidence_strings)
        constraints = getattr(case, "constraints", [])
        constraints_text = "\n".join(constraints) if constraints else "No explicit constraints provided."
        
        prompt = f"""You are a hostile, highly critical Adversarial Peer Reviewer.
Your sole job is to destroy the proposed hypothesis.

EVIDENCE:
{evidence_text}

CONSTRAINTS:
{constraints_text}

PROPOSED HYPOTHESIS:
Title: {hypothesis.title}
Rationale: {hypothesis.rationale}
Design: {hypothesis.experimental_design}
Expected Outcome: {hypothesis.expected_outcome}

Does this hypothesis violate ANY constraint or contradict the evidence?
Be brutal. If it uses future knowledge, reject it.

Respond ONLY with this exact JSON (no other text):
{{"critique": "your critique here", "approved": true}}
Set approved to true ONLY if the hypothesis perfectly survives all attacks."""
        try:
            schema_hint = {
                "critique": "string",
                "approved": False
            }
            data = self.gateway.query(prompt, schema_hint=schema_hint)
            return bool(data.get("approved", False))
        except Exception as e:
            print(f"Adversarial Peer Review failed: {e}. Defaulting to rejection.")
            return False

    def generate_hypothesis(self, case: HistoricalReplayCase, max_retries: int = 3, timeout_seconds: int = 180) -> GenerativeHypothesis | None:
        """
        De novo generation of a hypothesis, subjected to hostile peer review.
        Each attempt has a timeout to prevent infinite hangs with slow LLMs.
        """
        evidence_strings = [e.extracted_text if hasattr(e, "extracted_text") else str(e) for e in case.known_evidence]
        evidence_text = "\n".join(evidence_strings)
        constraints = getattr(case, "constraints", [])
        constraints_text = "\n".join(constraints) if constraints else "No explicit constraints provided."
        
        past_failures_text = "No prior failures recalled."
        if self.memory_system and hasattr(self.memory_system, 'recall_relevant_history'):
            import inspect
            if "case_time_window" in inspect.signature(self.memory_system.recall_relevant_history).parameters:
                past_failures = self.memory_system.recall_relevant_history(evidence_text, case_time_window=case.time_window)
            else:
                past_failures = self.memory_system.recall_relevant_history(evidence_text)
                
            if past_failures:
                past_failures_text = "\n".join(past_failures)

        prompt = f"""You are an autonomous Scientific Discovery Engine.
Synthesize the evidence and constraints to invent a novel experimental hypothesis.

DO NOT REPEAT PAST FAILURES:
{past_failures_text}

EVIDENCE:
{evidence_text}

CONSTRAINTS:
{constraints_text}

Invent the experiment that resolves the core epistemic tension.

Respond ONLY with this exact JSON format (no other text):
{{"title": "short title", "rationale": "why this resolves the tension", "experimental_design": "concrete steps", "expected_outcome": "what to expect if true"}}"""
        
        for attempt in range(max_retries):
            try:
                print(f"  Attempt {attempt + 1}/{max_retries}: Generating hypothesis...")
                data = self.gateway.query(prompt, schema_hint=GenerativeHypothesis)
                
                if isinstance(data, GenerativeHypothesis):
                    hypothesis = data
                else:
                    hypothesis = GenerativeHypothesis(**data)
                
                print(f"  Generated: '{hypothesis.title}'. Running adversarial review...")
                is_approved = self._hostile_peer_review(hypothesis, case)
                
                if is_approved:
                    print(f"  [PASS] Hypothesis '{hypothesis.title}' survived Hostile Peer Review on attempt {attempt + 1}!")
                    return hypothesis
                else:
                    print(f"  [FAIL] Attempt {attempt + 1}: Hypothesis rejected by Adversary.")
                    if self.memory_system and hasattr(self.memory_system, 'archive_failure'):
                        import inspect
                        if "case_time_window" in inspect.signature(self.memory_system.archive_failure).parameters:
                            self.memory_system.archive_failure(f"Hypothesis '{hypothesis.title}' failed adversarial review.", case.domain, case_time_window=case.time_window)
                        else:
                            self.memory_system.archive_failure(f"Hypothesis '{hypothesis.title}' failed adversarial review.", case.domain)
                    
            except Exception as e:
                print(f"  [ERR] Generation attempt {attempt + 1} failed: {e}")
                
        print("  Failed to generate a hypothesis that survives peer review.")
        return None
