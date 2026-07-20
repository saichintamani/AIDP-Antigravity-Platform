from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_GRAVITATIONAL_WAVES",
    domain="Astrophysics",
    time_window="1990-2015",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_GW_QUADRUPOLE_FORMULA",
            source_type="Publication",
            extracted_text="The strain amplitude h of a gravitational wave from a binary inspiral is given by the quadrupole formula. For a typical binary black hole merger at 400 Mpc, the expected maximum dimensionless strain is on the order of 10^-21.",
            ontology_tags=["General_Relativity", "Post_Newtonian_Expansion", "Astrophysics"],
            mathematical_constraints=["h_amplitude(400Mpc) ~= 1.0e-21", "h ∝ 1/D"]
        ),
        EpistemicEvidence(
            source_id="EV_GW_NUMERICAL_RELATIVITY",
            source_type="Publication",
            extracted_text="As the black holes enter the final plunge and merger, the post-Newtonian approximation breaks down. Exact waveforms for matched-filtering require solving the full non-linear Einstein equations via numerical relativity.",
            ontology_tags=["Numerical_Relativity", "Matched_Filtering", "Computational_Physics"],
            entity_relationships=["Strong_Field_Gravity -> breaks -> Post_Newtonian_Approximation"]
        ),
        EpistemicEvidence(
            source_id="EV_GW_SEISMIC_WALL",
            source_type="Publication",
            extracted_text="At frequencies below 40 Hz, terrestrial interferometers are overwhelmed by seismic noise (ground vibrations). Probing the 10-40 Hz band requires multi-stage active isolation (ISI) and quadruple pendulum suspensions achieving massive attenuation.",
            ontology_tags=["Experimental_Physics", "Seismic_Isolation", "Metrology"],
            mathematical_constraints=["Seismic_Noise_Cutoff(Initial_LIGO) == 40Hz", "Required_Attenuation(10Hz) >= 10^7"]
        ),
        EpistemicEvidence(
            source_id="EV_GW_STANDARD_QUANTUM_LIMIT",
            source_type="Publication",
            extracted_text="The Heisenberg Uncertainty Principle creates a Standard Quantum Limit (SQL) for the interferometer: high frequencies are dominated by photon shot noise (counting statistics), while low frequencies are dominated by quantum radiation pressure (photons kicking the 40kg test masses).",
            ontology_tags=["Quantum_Optics", "Standard_Quantum_Limit", "Heisenberg_Uncertainty"],
            entity_relationships=["Photon_Shot_Noise -> dominates -> High_Frequency", "Radiation_Pressure -> dominates -> Low_Frequency"]
        )
    ],
    hidden_outcome="Advanced LIGO, with upgraded seismic isolation and higher laser power, successfully detects a transient gravitational wave signal (GW150914) matching the inspiral and merger of two black holes.",
    constraints=[
        "Detector sensitivity must reach strain (h) of ~10^-21",
        "Detection must involve coincident signals at geographically separated sites",
        "Signal waveform must match General Relativity predictions for binary inspiral",
    ],
    candidate_experiments=[
        "Abandon terrestrial interferometers due to seismic noise and focus exclusively on launching space-based interferometers like LISA.",
        "Propose that gravitational waves interact with matter to create detectable electromagnetic flashes, and build wide-field optical telescopes to search for these flashes.",
        "Upgrade the terrestrial interferometers with active seismic isolation and higher-power lasers to reach the sensitivity required to detect binary black hole mergers.",
        "Argue that the Hulse-Taylor pulsar decay is due to unmodeled tidal friction, and cease funding for direct gravitational wave detection."
    ],
    historical_winner="Upgrade the terrestrial interferometers with active seismic isolation and higher-power lasers to reach the sensitivity required to detect binary black hole mergers.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Engineering-scale"
)
