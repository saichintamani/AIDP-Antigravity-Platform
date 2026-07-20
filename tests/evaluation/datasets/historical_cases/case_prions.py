from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_PRIONS",
    domain="Biology",
    time_window="1970-1981",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_TRANSMISSIBILITY",
            source_type="Publication",
            extracted_text="The agent causing Scrapie and Kuru is highly transmissible by inoculation into healthy animals, proving it is an infectious pathogen."
        ),
        EpistemicEvidence(
            source_id="EV_INCUBATION",
            source_type="Publication",
            extracted_text="The disease features an exceptionally long, silent incubation period (months to years) before rapid, fatal neurodegeneration."
        ),
        EpistemicEvidence(
            source_id="EV_RADIATION_RESISTANCE",
            source_type="Publication",
            extracted_text="The infectious agent is highly resistant to massive doses of ultraviolet (UV) and ionizing radiation—treatments that reliably destroy DNA and RNA."
        ),
        EpistemicEvidence(
            source_id="EV_HEAT_RESISTANCE",
            source_type="Publication",
            extracted_text="The agent survives boiling and standard formaldehyde sterilization, which typically inactivate conventional viruses."
        ),
        EpistemicEvidence(
            source_id="EV_CHEMICAL_SENSITIVITY",
            source_type="Publication",
            extracted_text="The agent's infectivity is destroyed by treatments that denature proteins (e.g., urea, phenol, proteases)."
        ),
        EpistemicEvidence(
            source_id="CONSTRAINT_CENTRAL_DOGMA",
            source_type="Publication",
            extracted_text="CONSTRAINT: The Central Dogma of molecular biology dictates that biological information flows from DNA to RNA to Protein. All infectious pathogens capable of replication must contain a nucleic acid genome."
        )
    ],
    hidden_outcome="The infectious agent lacks nucleic acid entirely and consists only of a self-replicating protein.",
    constraints=[
        "Agent must be resistant to UV radiation and nucleases (which destroy DNA/RNA)",
        "Agent must be inactivated by proteases and protein-denaturing agents",
        "Infection mechanism must not rely on nucleic acid translation",
    ],
    candidate_experiments=[
        "Assume the agent is a heavily shielded 'slow virus.' Design an intensive protocol using extreme physical disruption (ultracentrifugation and harsh detergents) to strip away the hypothetical protein coat and isolate the hidden viral DNA/RNA.",
        "Assume the agent is a plant-like viroid. Use highly sensitive radioactive nucleic acid hybridization probes across large volumes of infected brain homogenate to detect trace amounts of foreign, disease-specific RNA.",
        "Propose that the infectious agent is entirely devoid of nucleic acid and replicates through an unknown protein mechanism. Focus all efforts on purifying the disease-specific protein fraction and demonstrating that infectivity remains even after exhaustive nuclease digestion.",
        "Investigate the possibility that the disease is primarily an autoimmune reaction triggered by a persistent, slow-acting environmental toxin, and attempt to isolate the toxin using mass spectrometry."
    ],
    historical_winner="Propose that the infectious agent is entirely devoid of nucleic acid and replicates through an unknown protein mechanism. Focus all efforts on purifying the disease-specific protein fraction and demonstrating that infectivity remains even after exhaustive nuclease digestion.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Consensus-reversal"
)
