from typing import Any

from pydantic import BaseModel, Field


class HypothesisPayload(BaseModel):
    claim: str
    rationale: str
    confidence_prior: float
    evidence_links: list[str] = Field(default_factory=list)

class ControlGroup(BaseModel):
    type: str
    group_name: str
    isolated_variable: str
    purpose_and_justification: str

class SampleSizeRecommendation(BaseModel):
    n_per_group: int
    effect_size: Any # can be string or float
    significance_level_alpha: float
    target_power: float
    justification: str

class ExperimentDesign(BaseModel):
    independentVariables: list[str] = Field(default_factory=list)
    dependentVariables: list[str] = Field(default_factory=list)
    controls: list[ControlGroup] = Field(default_factory=list)
    failureCriteria: str = ""
    resourceEstimation: str = ""
    costPrediction: str = ""
    failurePrediction: str = ""
    # Fields added by Power Analyzer
    sample_size_recommendation: SampleSizeRecommendation | None = None
    control_isolation_validation: str = ""
    statistical_test: str = ""
    falsifiability_consistency_check: str = ""

class ReviewerCritique(BaseModel):
    reviewerName: str
    role: str
    confidence: float
    blockingIssues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    evidence: str
    riskScore: float
    decision: str # "approve" or "reject"

class ConsensusReport(BaseModel):
    consensusReached: bool
    finalDecision: str
    aggregatedRiskScore: float
    critiques: list[ReviewerCritique] = Field(default_factory=list)

class ProtocolStep(BaseModel):
    step_number: int
    description: str
    duration: str
    clinical_parameters: list[str] = Field(default_factory=list)

class ClinicalProtocol(BaseModel):
    treatment_arms: list[str] = Field(default_factory=list)
    comparator_arms: list[str] = Field(default_factory=list)
    blinding_strategy: str = ""
    randomization: str = ""
    successCriteria: str = ""
    inclusion_criteria: list[str] = Field(default_factory=list)
    exclusion_criteria: list[str] = Field(default_factory=list)
    primary_endpoints: list[str] = Field(default_factory=list)
    secondary_endpoints: list[str] = Field(default_factory=list)
    safety_monitoring_plan: str = ""
    protocol_steps: list[ProtocolStep] = Field(default_factory=list)

class EvidenceMapping(BaseModel):
    claim_component: str
    supporting_evidence: str

class EvidenceLinkage(BaseModel):
    evidence_to_claim_mapping: list[EvidenceMapping] = Field(default_factory=list)
    supporting_dois: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    evidence_confidence: str

class ControlGroupDef(BaseModel):
    group_name: str
    purpose: str

class Methodology(BaseModel):
    independent_variables: list[str] = Field(default_factory=list)
    dependent_variables: list[str] = Field(default_factory=list)
    control_groups: list[ControlGroupDef] = Field(default_factory=list)
    confounders_identified: list[str] = Field(default_factory=list)
    success_criteria: str

class StatsDesign(BaseModel):
    sample_size_recommendation: SampleSizeRecommendation
    control_isolation_validation: str
    statistical_test: str
    falsifiability_consistency_check: str

class Falsifiability(BaseModel):
    failure_criteria: str
    falsifiability_justification: str

class ControlTaxonomy(BaseModel):
    controls: list[ControlGroup] = Field(default_factory=list)

class EngineerFeasibility(BaseModel):
    resource_estimation: str
    cost_prediction: str
    failure_prediction: str
    critical_engineering_risks: list[str] = Field(default_factory=list)

class ExecutionProtocolModel(BaseModel):
    protocol_steps: list[ProtocolStep] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list, description="Explicit assumptions made during protocol generation")


class ClinicalMethodology(BaseModel):
    treatment_arms: list[str] = Field(default_factory=list)
    comparator_arms: list[str] = Field(default_factory=list)
    blinding_strategy: str
    randomization: str
    success_criteria: str

class ClinicalCohort(BaseModel):
    inclusion_criteria: list[str] = Field(default_factory=list)
    exclusion_criteria: list[str] = Field(default_factory=list)
    demographic_considerations: str

class ClinicalSafetyEfficacy(BaseModel):
    primary_endpoints: list[str] = Field(default_factory=list)
    secondary_endpoints: list[str] = Field(default_factory=list)
    safety_monitoring_plan: str