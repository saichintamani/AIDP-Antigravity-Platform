from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_HELICASE",
    domain="Biochemistry",
    time_window="1970-1979",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_HELICASE_THERMODYNAMICS",
            source_type="Publication",
            extracted_text="The hydrogen bonds holding the DNA duplex together are highly stable; spontaneous unwinding at physiological temperatures is thermodynamically forbidden, especially ahead of a replication fork moving at 1000 base pairs per second.",
            ontology_tags=["Biophysics", "Thermodynamics", "Replication_Fork"],
            mathematical_constraints=["Delta_G_melting(37C) > 0", "Fork_Speed == 1000_bp/sec"]
        ),
        EpistemicEvidence(
            source_id="EV_HELICASE_ATP_REQUIREMENT",
            source_type="Publication",
            extracted_text="In vitro DNA replication assays have demonstrated an absolute requirement for ATP hydrolysis, even when the polymerase itself does not consume ATP for polymerization. The Rep protein exhibits single-stranded DNA-dependent ATPase activity, yielding -30.5 kJ/mol.",
            ontology_tags=["Enzymology", "In_Vitro_Assays", "ATP_Hydrolysis"],
            mathematical_constraints=["Delta_G(ATP_Hydrolysis) == -30.5_kJ/mol", "Replication_Rate(ATP_depleted) == 0"]
        ),
        EpistemicEvidence(
            source_id="EV_HELICASE_REP_MUTANT",
            source_type="Publication",
            extracted_text="Certain E. coli mutants (rep) are severely defective in DNA replication but possess fully functional DNA polymerases and ligases.",
            ontology_tags=["Genetics", "Microbiology", "Mutagenesis"],
            entity_relationships=["rep_Gene_Mutation -> impairs -> DNA_Replication", "DNA_Polymerase -> is_functional_in -> rep_Mutant"]
        ),
        EpistemicEvidence(
            source_id="EV_HELICASE_DIMER_ROTATION",
            source_type="Publication",
            extracted_text="Structural predictions suggest that a functional unwinding motor would likely operate as an oligomer, undergoing massive conformational changes powered by ATP to continuously translocate on DNA.",
            ontology_tags=["Structural_Biology", "Protein_Dynamics", "Conformational_Change"],
            mathematical_constraints=["Oligomeric_State >= 2"]
        )
    ],
    hidden_outcome="There exists a specific class of enzymes (DNA helicases, specifically Rep protein) that are molecular motors. They couple the hydrolysis of ATP to the mechanical separation of the DNA double helix, operating actively rather than relying on thermal fluctuations or polymerase wedging (Takahashi et al. 1979).",
    constraints=[
        "Separation of DNA strands must couple with ATP hydrolysis",
        "Separation rate must be significantly faster than thermal breathing alone",
        "Enzyme must act actively, not passively waiting for fluctuations",
    ],
    candidate_experiments=[
        "Assume DNA strands spontaneously 'breathe' open due to thermal fluctuations at physiological temperatures, allowing SSBs to passively trap the single strands, and measure binding kinetics.",
        "Propose that DNA polymerase itself physically forces the strands apart as it moves forward, requiring no independent unwinding enzyme, and utilizing the energy of dNTP incorporation.",
        "Purify the rep protein and demonstrate that it acts as a dedicated molecular motor, coupling the hydrolysis of ATP directly to the active mechanical separation of the DNA double helix.",
        "Investigate if the Rep protein simply degrades the complementary DNA strand entirely to allow the polymerase to easily copy the remaining single strand without needing unwinding."
    ],
    historical_winner="Purify the rep protein and demonstrate that it acts as a dedicated molecular motor, coupling the hydrolysis of ATP directly to the active mechanical separation of the DNA double helix.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Paradigm-shift"
)
