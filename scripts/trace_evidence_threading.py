"""
Evidence Threading Diagnostic Trace
====================================
Follows DOIs through: Retrieval -> Prompt -> Model -> Hypothesis -> Governance
Purpose: Identify exactly where citations get lost.
"""
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from aidp.knowledge.connectors.pubmed_connector import PubMedConnector
from aidp.intelligence.prompts.registry import PromptRegistry
from aidp.discovery.hypothesis import HypothesisGenerator
from aidp.intelligence.providers.routing import RoutingPolicy
from aidp.intelligence.providers.middleware import IntelligenceGateway
from aidp.intelligence.providers.llm import LLMProvider
from aidp.intelligence.providers.capabilities import ProviderCapabilities, ReasoningTier
from aidp.governance.engine import ScientificGovernanceEngine


def main():
    print("=" * 70)
    print("EVIDENCE THREADING DIAGNOSTIC TRACE")
    print("=" * 70)

    # Stage 1: Retrieval
    print("\n## STAGE 1: RETRIEVAL")
    connector = PubMedConnector(max_results=3)
    query = "KRAS G12C Sotorasib"
    provenance_entries = connector.fetch_literature_provenance(query)
    
    documents = []
    dois_at_retrieval = []
    for entry in provenance_entries:
        doc = {
            "source_doi": entry.source_paper_doi,
            "text": entry.claim_text[:200],
            "title": entry.retriever_metadata.get("title")
        }
        documents.append(doc)
        dois_at_retrieval.append(entry.source_paper_doi)
    
    knowledge_context = {"query": query, "documents": documents}
    
    print(f"Papers retrieved: {len(documents)}")
    for i, doi in enumerate(dois_at_retrieval):
        print(f"  DOI[{i}]: {doi}")
    
    # Stage 2: Prompt Construction
    print("\n## STAGE 2: PROMPT CONSTRUCTION")
    
    contradiction = {"id": "c1", "description": f"Contradiction related to {query}"}
    context_dict = {
        "contradiction": json.dumps(contradiction),
        "retrieved_knowledge": json.dumps(knowledge_context)
    }
    
    pt = PromptRegistry.get("hypothesis_generator")
    
    has_rk_placeholder = "{retrieved_knowledge}" in pt.template
    print(f"Template has retrieved_knowledge placeholder: {has_rk_placeholder}")
    
    dois_in_prompt = []
    try:
        rendered_prompt = pt.render(context_dict)
        print(f"Prompt rendered successfully: {len(rendered_prompt)} chars")
        
        for doi in dois_at_retrieval:
            if doi in rendered_prompt:
                dois_in_prompt.append(doi)
        
        print(f"DOIs present in rendered prompt: {len(dois_in_prompt)}/{len(dois_at_retrieval)}")
        for doi in dois_in_prompt:
            print(f"  FOUND: {doi}")
        for doi in dois_at_retrieval:
            if doi not in dois_in_prompt:
                print(f"  MISSING: {doi}")
        
        print(f"\n--- RENDERED PROMPT ---")
        print(rendered_prompt[:500])
        print("--- END PROMPT ---")
        
    except KeyError as e:
        print(f"Template render FAILED: missing key {e}")
        rendered_prompt = None

    # Stage 3: Model Response
    print("\n## STAGE 3: MODEL RESPONSE")
    
    routing_policy = RoutingPolicy()
    llm_provider = LLMProvider(model_name="ollama/llama3.2:3b", api_key="dummy")
    caps = ProviderCapabilities(
        structured_output=True, tool_calling=False, streaming=False,
        vision=False, max_context=8000, supports_json_schema=True,
        reasoning_tier=ReasoningTier.EXPERT,
        cost_per_1m_input_tokens=0.0, cost_per_1m_output_tokens=0.0
    )
    routing_policy.register_provider("primary_local", llm_provider, caps)
    gateway = IntelligenceGateway(routing_policy=routing_policy)
    
    generator = HypothesisGenerator(gateway=gateway)
    hypotheses = generator.generate_from_contradiction(contradiction, knowledge_context)
    
    dois_in_hypothesis = []
    if hypotheses:
        h = hypotheses[0]
        print(f"Hypothesis generated: YES")
        print(f"Claim: {h.get('claim', 'N/A')[:200]}")
        print(f"evidence_links: {h.get('evidence_links', 'KEY MISSING')}")
        print(f"provenance_chain: {h.get('provenance_chain', 'KEY MISSING')}")
        
        # Stage 4: DOI comparison
        print("\n## STAGE 4: DOI CHAIN COMPARISON")
        
        hyp_links = h.get("evidence_links", [])
        hyp_prov = h.get("provenance_chain", [])
        
        for doi in dois_at_retrieval:
            found_in_links = any(doi in str(link) for link in hyp_links)
            found_in_prov = any(doi in str(p) for p in hyp_prov)
            if found_in_links or found_in_prov:
                dois_in_hypothesis.append(doi)
        
        print(f"DOIs surviving to hypothesis: {len(dois_in_hypothesis)}/{len(dois_at_retrieval)}")
        for doi in dois_at_retrieval:
            status = "SURVIVED" if doi in dois_in_hypothesis else "LOST"
            print(f"  {status}: {doi}")
        
        # Stage 5: Governance
        print("\n## STAGE 5: GOVERNANCE INPUT")
        governance = ScientificGovernanceEngine()
        passed, reason = governance.evaluate_hypothesis(h)
        print(f"Governance result: {'PASSED' if passed else 'REJECTED'}")
        print(f"Reason: {reason}")
        
        ev_links = h.get("evidence_links", [])
        print(f"\nEvidenceChecker input: evidence_links = {ev_links}")
        print(f"EvidenceChecker truthy? {bool(ev_links)}")
        
    else:
        print("No hypothesis generated")
    
    # Summary
    print("\n" + "=" * 70)
    print("DIAGNOSIS SUMMARY")
    print("=" * 70)
    print(f"DOIs at Retrieval:  {len(dois_at_retrieval)}")
    print(f"DOIs in Prompt:     {len(dois_in_prompt)}")
    print(f"DOIs in Hypothesis: {len(dois_in_hypothesis)}")
    
    if not has_rk_placeholder:
        print("\nROOT CAUSE: Prompt template lacks retrieved_knowledge placeholder.")
        print("   The model never sees the retrieved papers or DOIs.")


if __name__ == "__main__":
    main()
