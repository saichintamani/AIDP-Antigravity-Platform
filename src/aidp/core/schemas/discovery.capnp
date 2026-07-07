@0xb1f9b3b8f1c8e2a1;

struct KnowledgeGap {
    id @0 :Text;
    conceptA @1 :Text;
    conceptB @2 :Text;
    estimatedEntropy @3 :Float64; # Higher means more unknown
    confidenceMissing @4 :Float64;
    description @5 :Text;
}

struct Contradiction {
    id @0 :Text;
    claimA @1 :Text;
    sourceAId @2 :Text;
    claimB @3 :Text;
    sourceBId @4 :Text;
    contradictionScore @5 :Float64; # 1.0 = direct logical contradiction
    resolutionHypothesis @6 :Text;
}

struct Hypothesis {
    id @0 :Text;
    claim @1 :Text;
    supportingEvidenceIds @2 :List(Text);
    opposingEvidenceIds @3 :List(Text);
    confidence @4 :Float64;
    risk @5 :Float64;
    expectedInformationGain @6 :Float64;
}

struct CompetingHypotheses {
    groupId @0 :Text;
    hypotheses @1 :List(Hypothesis);
}

struct CausalGraph {
    nodes @0 :List(Text);
    directedEdges @1 :List(Text); # Format "A->B"
    unobservedConfounders @2 :List(Text); # Format "U->A,B"
}

struct CounterfactualIntervention {
    targetVariable @0 :Text;
    interventionValue @1 :Float64;
    expectedEffect @2 :Float64;
}

struct ExperimentalDesign {
    id @0 :Text;
    hypothesisId @1 :Text;
    independentVariables @2 :List(Text);
    dependentVariables @3 :List(Text);
    controls @4 :List(Text);
    failureCriteria @5 :Text;
}

struct ActiveDiscoveryTask {
    id @0 :Text;
    experimentalDesignId @1 :Text;
    expectedInformationGain @2 :Float64;
    executionCost @3 :Float64;
}

enum ReadinessLevel {
    insufficientEvidence @0;
    needsRetrieval @1;
    needsContradictionResolution @2;
    readyForCausal @3;
    readyForExperiment @4;
}

struct HypothesisQuality {
    novelty @0 :Float64;
    logicalConsistency @1 :Float64;
    testability @2 :Float64;
    falsifiability @3 :Float64;
    scientificPlausibility @4 :Float64;
}

struct HypothesisLedgerEntry {
    hypothesisId @0 :Text;
    quality @1 :HypothesisQuality;
    readiness @2 :ReadinessLevel;
    invalidationCriteria @3 :List(Text);
    redundancyCollapsedIds @4 :List(Text);
    provenanceHash @5 :Text;
}

struct ReviewerCritique {
    role @0 :Text;
    severity @1 :Text;  # "low", "medium", "critical"
    feedback @2 :Text;
    isBlocking @3 :Bool;
}

struct DebateRecord {
    experimentalDesignId @0 :Text;
    critiques @1 :List(ReviewerCritique);
    consensusReached @2 :Bool;
    finalDecision @3 :Text; # "approved", "rejected", "needs_revision"
}
