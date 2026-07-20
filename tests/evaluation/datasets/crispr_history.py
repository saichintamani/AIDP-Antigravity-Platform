from aidp.intelligence.epistemic_models import EpistemicEvidence

crispr_dataset = [
    # T=1987 (Ishino et al.)
    EpistemicEvidence(
        source_id="EV_CRISPR_1987",
        source_type="Publication",
        extracted_text="Sequence of the iap gene in E. coli reveals an unusual series of 29-bp repeats separated by 32-bp non-repetitive spacer sequences."
    ),
    # T=1993 (Mojica et al.)
    EpistemicEvidence(
        source_id="EV_CRISPR_1993",
        source_type="Publication",
        extracted_text="Similar 30-bp repeats are found in Haloferax mediterranei. They appear to be evolutionarily conserved across distantly related archaea and bacteria, suggesting a major biological function."
    ),
    # T=2002 (Jansen et al.)
    EpistemicEvidence(
        source_id="EV_CRISPR_2002",
        source_type="Publication",
        extracted_text="These repeats (now called CRISPR) are strictly associated with a set of homologous genes (cas genes). The cas genes encode putative nucleases and helicases."
    ),
    # T=2005 (Mojica / Pourcel / Bolotin)
    EpistemicEvidence(
        source_id="EV_CRISPR_2005",
        source_type="Publication",
        extracted_text="The non-repetitive spacer sequences between the CRISPR repeats show exact sequence homology to known bacteriophages and plasmids. Strains possessing a spacer matching a specific phage are resistant to that phage."
    )
    # T=2007 (Barrangou et al.) is intentionally omitted. This is the conclusion we are testing if the system can predict.
]
