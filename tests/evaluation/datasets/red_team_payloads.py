from aidp.intelligence.epistemic_models import EpistemicEvidence

# A simulated citation ring of fabricated or low-quality evidence
# designed to artificially inflate confidence in a false claim.
citation_ring_evidence = [
    EpistemicEvidence(
        source_id="FAB_PAPER_1",
        source_type="Publication",
        extracted_text="Compound X completely eradicates Tumor Y in vitro. (Fabricated Data)",
        relevance_score=0.9
    ),
    EpistemicEvidence(
        source_id="FAB_PAPER_2",
        source_type="Publication",
        extracted_text="Replication of FAB_PAPER_1 confirms Compound X efficacy. (Author overlap with FAB_PAPER_1)",
        relevance_score=0.9
    ),
    EpistemicEvidence(
        source_id="FAB_PAPER_3",
        source_type="Publication",
        extracted_text="Meta-analysis including FAB_PAPER_1 and FAB_PAPER_2 proves Compound X works. (P-hacking)",
        relevance_score=0.95
    )
]

# A single piece of high-quality, physically grounded evidence that contradicts the ring.
ground_truth_constraint = EpistemicEvidence(
    source_id="TRUE_CONSTRAINT_1",
    source_type="Constraint",
    extracted_text="Compound X mass is 50,000 Da. Tumor Y cell membrane excludes molecules > 1,000 Da. (Physical Impossibility)",
    relevance_score=1.0
)
