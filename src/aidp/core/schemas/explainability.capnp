@0xa5df1762c2f461be;

using CognitiveObject = import "cognitive_object.capnp".CognitiveObject;

struct FeatureAttribution {
    vectorSimilarity @0 :Float64;
    keywordContribution @1 :Float64;
    graphTraversal @2 :Float64;
    metadataFilters @3 :Float64;
    recency @4 :Float64;
    citationScore @5 :Float64;
    confidence @6 :Float64;
}

struct UncertaintyAttribution {
    model @0 :Float64;
    retrieval @1 :Float64;
    knowledge @2 :Float64;
    tool @3 :Float64;
    planning @4 :Float64;
    observation @5 :Float64;
}

struct ExplainableRetrievalResult {
    id @0 :Text;
    cognitiveObject @1 :CognitiveObject;
    rank @2 :Int32;
    reasonRetrieved @3 :Text;
    featureAttribution @4 :FeatureAttribution;
}

struct ReasonTraceStep {
    id @0 :Text;
    observation @1 :Text;
    retrievedEvidence @2 :List(ExplainableRetrievalResult);
    inference @3 :Text;
    hypothesis @4 :Text;
    alternativesConsidered @5 :List(Text);
    confidenceUpdate @6 :Float64;
    action @7 :Text;
    counterfactualDependency @8 :Bool; # Would this step occur without the retrieved evidence?
    uncertainty @9 :UncertaintyAttribution;
}

struct ReasonTrace {
    id @0 :Text;
    query @1 :Text;
    steps @2 :List(ReasonTraceStep);
    finalDecision @3 :Text;
    globalUncertainty @4 :UncertaintyAttribution;
    reflection @5 :Text;
    memoryUpdates @6 :List(Text);
    timestamp @7 :Float64;
}
