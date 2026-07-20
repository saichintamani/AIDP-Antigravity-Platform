from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_RNAI",
    domain="Molecular Biology",
    time_window="1990-1998",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_RNAI_ANTISENSE",
            source_type="Publication",
            extracted_text="Antisense RNA (single-stranded RNA complementary to an mRNA) is known to inhibit gene expression by stoichiometrically binding the mRNA and preventing translation via 1:1 steric hindrance.",
            ontology_tags=["Molecular_Biology", "Gene_Silencing", "Antisense_Therapy"],
            entity_relationships=["Antisense_RNA -> inhibits -> Translation"],
            mathematical_constraints=["Silencing_Ratio(Antisense_RNA, mRNA) == 1:1"]
        ),
        EpistemicEvidence(
            source_id="EV_RNAI_COSUPPRESSION",
            source_type="Publication",
            extracted_text="In petunias, introducing extra copies of a chalcone synthase gene paradoxically suppresses both the endogenous gene and the introduced gene, causing white flowers. This is termed 'cosuppression' (Napoli et al. 1990).",
            ontology_tags=["Genetics", "Botany", "Epigenetics", "Cosuppression"],
            entity_relationships=["Transgene -> suppresses -> Endogenous_Gene"],
            mathematical_constraints=["Expression_Level(Transgene + Endogenous) == 0"]
        ),
        EpistemicEvidence(
            source_id="EV_RNAI_NEMATODE_ANOMALY",
            source_type="Publication",
            extracted_text="In C. elegans, injecting 'sense' par-1 RNA (identical to mRNA) surprisingly causes the same silencing effect as injecting 'antisense' RNA (Guo & Kemphues 1995).",
            ontology_tags=["Molecular_Biology", "Nematology", "Experimental_Anomaly"],
            mathematical_constraints=["Silencing_Effect(Sense_RNA) == Silencing_Effect(Antisense_RNA)"]
        ),
        EpistemicEvidence(
            source_id="EV_RNAI_PREPARATIONS",
            source_type="Publication",
            extracted_text="RNA preparations synthesized in vitro often contain trace amounts of double-stranded RNA (dsRNA) as a byproduct of the T7 polymerase reaction.",
            ontology_tags=["Biochemistry", "In_Vitro_Transcription", "Contaminants"],
            entity_relationships=["T7_Polymerase -> produces -> dsRNA_Byproduct"]
        )
    ],
    hidden_outcome="The actual trigger for potent and specific gene silencing is double-stranded RNA (dsRNA), which activates the RNA interference (RNAi) pathway to catalytically destroy matching mRNAs. The effect is sub-stoichiometric, requiring only a few dsRNA molecules per cell (Fire et al., 1998).",
    constraints=[
        "Silencing must be sub-stoichiometric (a few molecules silence abundant mRNA)",
        "Sense and antisense RNA individually are inefficient; they must act together",
        "The trigger must be highly specific to the target sequence",
    ],
    candidate_experiments=[
        "Hypothesize that 'sense' RNA injections act as a sponge for naturally occurring endogenous antisense RNA, disrupting a natural homeostatic equilibrium, and test this by measuring endogenous antisense levels.",
        "Propose that cosuppression and sense-silencing are caused by transcriptional silencing via DNA methylation triggered by high concentrations of ectopic RNA molecules targeting the promoter.",
        "Test highly purified double-stranded RNA (dsRNA) against highly purified single-stranded RNA, hypothesizing that trace dsRNA is the true, highly potent trigger for gene silencing acting via a sub-stoichiometric (catalytic) destruction of mRNA.",
        "Investigate whether the introduction of any foreign RNA simply over-activates a generic antiviral ribonuclease (RNase L) that indiscriminately degrades all mRNA in the cytoplasm."
    ],
    historical_winner="Test highly purified double-stranded RNA (dsRNA) against highly purified single-stranded RNA, hypothesizing that trace dsRNA is the true, highly potent trigger for gene silencing acting via a sub-stoichiometric (catalytic) destruction of mRNA.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Paradigm-shift"
)
