from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_CRISPR",
    domain="Molecular Biology & Gene Editing",
    time_window="2010-2012",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_CRISPR_DUAL_RNA",
            source_type="Publication",
            extracted_text="Biochemical isolation of the Cas9 complex reveals that it strictly requires TWO separate RNA molecules to function: a CRISPR RNA (crRNA) that contains the 20-nucleotide targeting sequence, and a trans-activating CRISPR RNA (tracrRNA) that forms a structural scaffold to lock into Cas9.",
            ontology_tags=["Biochemistry", "crRNA", "tracrRNA"],
            entity_relationships=["Cas9_Activation -> requires -> (crRNA AND tracrRNA)"]
        ),
        EpistemicEvidence(
            source_id="EV_CRISPR_CLEAVAGE_DOMAINS",
            source_type="Publication",
            extracted_text="Cas9 utilizes two distinct nuclease domains: the HNH domain cleaves the DNA strand complementary to the crRNA guide, while the RuvC-like domain cleaves the non-complementary DNA strand.",
            ontology_tags=["Structural_Biology", "HNH_Domain", "RuvC_Domain", "Endonuclease"]
        ),
        EpistemicEvidence(
            source_id="EV_CRISPR_RNA_BASEPAIRING",
            source_type="Publication",
            extracted_text="The crRNA and tracrRNA interact via a short stretch of complementary base-pairing to form a stable duplex. Structural modeling indicates the 3' end of the crRNA and the 5' end of the tracrRNA are approximately 40 Ångströms apart.",
            ontology_tags=["Structural_Biology", "RNA_Duplex", "Distance_Constraints"],
            mathematical_constraints=["Distance(3_prime_crRNA, 5_prime_tracrRNA) ~= 40_Angstroms"]
        )
    ],
    hidden_outcome="The two separate RNA molecules can be artificially fused together. A highly specific synthetic linker—a GAAA tetraloop—can bridge the 40 Ångström gap without disrupting the secondary structure, creating a Single-Guide RNA (sgRNA) that transforms Cas9 into a programmable gene editing tool.",
    constraints=[
        "Cas9 requires BOTH crRNA AND tracrRNA simultaneously to function",
        "Distance(3_prime_crRNA, 5_prime_tracrRNA) ~= 40 Angstroms",
        "HNH domain cleaves complementary strand; RuvC cleaves non-complementary strand",
        "Any linker must preserve the crRNA:tracrRNA duplex secondary structure",
    ],
    candidate_experiments=[
        "Attempt to deliver Cas9 protein along with separate crRNA and tracrRNA transcripts into mammalian cells, relying on spontaneous self-assembly.",
        "Engineer the Cas9 protein to directly bind double-stranded DNA without needing any RNA guides, to simplify the system for gene editing.",
        "Covalently link the 3' end of the crRNA to the 5' end of the tracrRNA using a synthetic GAAA tetraloop to bridge the 40 Å gap, creating a Single-Guide RNA (sgRNA) that programs Cas9 cleavage.",
        "Mutate the tracrRNA sequence to make it universally bind to any host genomic DNA, turning Cas9 into a random mutagen."
    ],
    historical_winner="Covalently link the 3' end of the crRNA to the 5' end of the tracrRNA using a synthetic GAAA tetraloop to bridge the 40 Å gap, creating a Single-Guide RNA (sgRNA) that programs Cas9 cleavage.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Paradigm-shift"
)
