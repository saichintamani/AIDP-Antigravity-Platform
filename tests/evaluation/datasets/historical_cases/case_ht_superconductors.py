from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_HT_SUPERCONDUCTORS",
    domain="Condensed Matter Physics",
    time_window="1980-1986",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_HTSC_MCMILLAN_LIMIT",
            source_type="Publication",
            extracted_text="The Eliashberg-McMillan formulation of BCS theory dictates that the critical temperature (Tc) of phonon-mediated superconductors is bounded by lattice instabilities. As the electron-phonon coupling constant (λ) increases, structural phase transitions cap the theoretical maximum Tc at approximately 30 K.",
            ontology_tags=["BCS_Theory", "Eliashberg_McMillan_Equation", "Theoretical_Limits"],
            mathematical_constraints=["T_c(Max_BCS) <= 30K", "Electron_Phonon_Coupling(λ) -> causes -> Lattice_Instability"]
        ),
        EpistemicEvidence(
            source_id="EV_HTSC_NB3GE_RECORD",
            source_type="Publication",
            extracted_text="The highest experimentally confirmed superconducting transition temperature to date is 23.2 K, achieved in the A15-phase intermetallic alloy Nb3Ge. Over a decade of metallurgy has failed to push past this barrier.",
            ontology_tags=["Materials_Science", "Metallurgy", "A15_Phases"],
            mathematical_constraints=["Max_Tc_Observed(Intermetallics) == 23.2K"]
        ),
        EpistemicEvidence(
            source_id="EV_HTSC_CUPRATE_INSULATORS",
            source_type="Publication",
            extracted_text="Lanthanum-based cuprate perovskites, specifically the composition La_{5-x}Ba_xCu_5O_{5(3-y)}, are typically classified as Mott insulators. In the standard paradigm, insulating metal oxides lack the free electron density required for conventional metallic superconductivity.",
            ontology_tags=["Condensed_Matter_Physics", "Mott_Insulators", "Cuprate_Perovskites"],
            entity_relationships=["Cuprate_Perovskites -> exhibit -> Mott_Insulator_Behavior", "Insulators -> contradict -> Standard_Metallic_Superconductivity"]
        ),
        EpistemicEvidence(
            source_id="EV_HTSC_JAHN_TELLER_POLARONS",
            source_type="Publication",
            extracted_text="It is hypothesized that substituting Barium (Ba) for Lanthanum (La) in certain copper-oxide ceramics might trigger strong Jahn-Teller interactions, creating localized polarons that could mediate electron pairing via non-phononic mechanisms.",
            ontology_tags=["Solid_State_Chemistry", "Jahn_Teller_Effect", "Polaronic_Conduction"],
            entity_relationships=["Barium_Substitution -> induces -> Jahn_Teller_Polarons", "Jahn_Teller_Polarons -> mediate -> Non_Phononic_Pairing"]
        )
    ],
    hidden_outcome="Doping a ceramic insulator (La-Ba-Cu-O) creates a cuprate superconductor with a Tc of 35K, shattering the theoretical limit and opening the era of high-Tc superconductivity.",
    constraints=[
        "Tc must exceed the theoretical BCS limit of ~30K",
        "Material must exhibit perfect diamagnetism (Meissner effect)",
        "Material must have zero electrical resistance below Tc",
    ],
    candidate_experiments=[
        "Continue substituting transition metals in A15-structure intermetallic compounds (like Nb3Ge) to incrementally optimize the electron density of states.",
        "Focus on synthesizing ultra-pure elemental metals and applying extreme high pressures to force electron-phonon coupling to higher limits.",
        "Synthesize mixed-valence copper-oxide perovskite ceramics (like Ba-La-Cu-O) and test them for superconductivity, hypothesizing that strong Jahn-Teller interactions could lead to high-Tc.",
        "Abandon phonon-mediated superconductivity entirely and attempt to build organic polymer superconductors based on purely excitonic pairing mechanisms."
    ],
    historical_winner="Synthesize mixed-valence copper-oxide perovskite ceramics (like Ba-La-Cu-O) and test them for superconductivity, hypothesizing that strong Jahn-Teller interactions could lead to high-Tc.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Domain-blindspot"
)
