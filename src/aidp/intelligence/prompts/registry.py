import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass
class PromptTemplate:
    """
    A versioned prompt template.
    Tracks the hash of the template to ensure exact provenance during replay.
    """

    name: str
    template: str

    @property
    def version_hash(self) -> str:
        return hashlib.sha256(self.template.encode("utf-8")).hexdigest()[:8]

    def render(self, variables: dict[str, Any]) -> str:
        """Renders the template with the provided variables."""
        return self.template.format(**variables)


class PromptRegistry:
    """Central registry for all prompts to ensure they are versioned."""

    _prompts: dict[str, PromptTemplate] = {}

    @classmethod
    def register(cls, name: str, template: str) -> PromptTemplate:
        pt = PromptTemplate(name=name, template=template)
        cls._prompts[name] = pt
        return pt

    @classmethod
    def get(cls, name: str) -> PromptTemplate:
        return cls._prompts[name]


# Register standard prompts
PromptRegistry.register(
    name="experiment_planner",
    template="""
You are an expert Scientific Methodologist. Design a strict empirical experiment to test the following hypothesis claim:
Claim: "{claim}"

Return a JSON object with exactly the following keys:
- "independentVariables": A list of strings.
- "dependentVariables": A list of strings.
- "controls": A list of strings detailing control conditions.
- "failureCriteria": A strict string detailing exactly what empirical result would falsify the claim.
- "resourceEstimation": A string detailing the required lab equipment, datasets, or compute.
- "costPrediction": A string indicating the expected cost (qualitative or quantitative).
- "failurePrediction": A string describing operational or execution risks (distinct from scientific falsification).
""",
)

PromptRegistry.register(
    name="statistician_review",
    template="""
You are a harsh Statistician reviewing an experimental design.
Variables: {variables}
Controls: {controls}
Sample Size: {sample_size}
Metrics: {metrics}
Check for strict control groups and mathematically falsifiable failure criteria.
Return JSON with keys: 'reviewerName', 'role', 'confidence' (float), 'blockingIssues' (list), 'suggestions' (list), 'evidence' (string), 'riskScore' (float), 'decision' (approve/reject).
""",
)
PromptRegistry.register(
    name="domain_expert_review",
    template="""
You are a Domain Expert reviewing an experimental design for biological/physical plausibility.
Scientific Claim: {claim}
Hypothesis: {hypothesis}
Evidence: {evidence}
Return JSON with keys: 'reviewerName', 'role', 'confidence' (float), 'blockingIssues' (list), 'suggestions' (list), 'evidence' (string), 'riskScore' (float), 'decision' (approve/reject).
""",
)

PromptRegistry.register(
    name="methodologist_review",
    template="""
You are a Methodologist reviewing an experimental design.
Protocol: {protocol}
Experiment Flow: {experiment_flow}
Confounders: {confounders}
Check for unmeasured confounders and ensure independent variables are actually manipulated.
Return JSON with keys: 'reviewerName', 'role', 'confidence' (float), 'blockingIssues' (list), 'suggestions' (list), 'evidence' (string), 'riskScore' (float), 'decision' (approve/reject).
""",
)

PromptRegistry.register(
    name="ethicist_review",
    template="""
You are an Ethicist reviewing an experimental design.
Protocol: {protocol}
Resource Requirements: {resources}
Check for ethical implications, risk of dual-use, and participant safety.
Return JSON with keys: 'reviewerName', 'role', 'confidence' (float), 'blockingIssues' (list), 'suggestions' (list), 'evidence' (string), 'riskScore' (float), 'decision' (approve/reject).
""",
)

PromptRegistry.register(
    name="engineer_review",
    template="""
You are an Engineer reviewing an experimental design for technical feasibility.
Protocol: {protocol}
Resource Requirements: {resources}
Cost Prediction: {cost_prediction}
Failure Prediction: {failure_prediction}
Check for feasibility, technical implementation, and automation compatibility.
Return JSON with keys: 'reviewerName', 'role', 'confidence' (float), 'blockingIssues' (list), 'suggestions' (list), 'evidence' (string), 'riskScore' (float), 'decision' (approve/reject).
""",
)

PromptRegistry.register(
    name="hypothesis_generator",
    template="""
You are a Scientific Hypothesis Generator.

Given the following identified contradiction in the knowledge graph:
Contradiction: {contradiction}

The following papers were retrieved as evidence. You MUST cite them using their DOIs.

Retrieved Evidence:
{retrieved_knowledge}

Generate a novel, testable scientific hypothesis that resolves this contradiction.
You MUST reference the DOIs from the retrieved evidence above.

Return a JSON object with exactly these keys:
- "claim": A strictly falsifiable scientific claim.
- "rationale": The reasoning linking the contradiction to this claim, referencing the retrieved evidence.
- "confidence_prior": A float between 0.0 and 1.0.
- "evidence_links": A list of DOI strings from the retrieved evidence above that support your claim. DO NOT invent DOIs. Use only the DOIs provided above.
""",
)

PromptRegistry.register(
    name="evidence_linkage_validator",
    template="""
You are a Scientific Evidence Linkage Validator.
Your job is to ensure that a proposed scientific hypothesis is strictly grounded in the retrieved literature.

Claim: "{claim}"
Rationale: "{rationale}"
Retrieved Evidence:
{evidence}

Return a JSON object with exactly the following keys:
- "evidence_to_claim_mapping": A list of objects, each with "claim_component" (string) and "supporting_evidence" (string quote from text).
- "supporting_dois": A list of strings (DOIs) from the retrieved evidence that support the claim.
- "unsupported_claims": A list of strings detailing any part of the hypothesis that lacks evidence in the retrieved text.
- "evidence_confidence": A string ("High", "Medium", "Low") summarizing the grounding strength.
""",
)

PromptRegistry.register(
    name="methodology_generator",
    template="""
You are an Experimental Methodology Generator.
Your job is to translate a grounded hypothesis into a rigorous experimental scaffolding, ensuring strict controls and identifying confounders.

Claim: "{claim}"
Evidence Mapping:
{evidence_mapping}

Return a JSON object with exactly the following keys:
- "independent_variables": A list of strings.
- "dependent_variables": A list of strings.
- "control_groups": A list of objects, each with "group_name" (string) and "purpose" (string).
- "confounders_identified": A list of strings identifying potential unmeasured confounders.
- "success_criteria": A string defining exactly what must be observed to support the hypothesis.
""",
)

PromptRegistry.register(
    name="statistical_validator",
    template="""
You are a Statistical Design Validator.
Your job is to define the quantitative and statistical framework for a proposed experimental methodology.

Experimental Methodology:
{methodology}

Return a JSON object with exactly the following keys:
- "sample_size_recommendation": An object with "n_per_group" (integer, provide a realistic estimate e.g., 30, 100) and "justification" (string).
- "statistical_test": A string naming the specific statistical test to use (e.g., "Two-way ANOVA").
- "power_considerations": A string discussing statistical power and effect size.
- "reproducibility_notes": A string outlining how to ensure this experiment can be independently replicated.
""",
)
