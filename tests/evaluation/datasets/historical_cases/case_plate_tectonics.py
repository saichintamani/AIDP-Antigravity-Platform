from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_PLATE_TECTONICS",
    domain="Earth Science",
    time_window="1950-1963",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_PT_STATIC",
            source_type="Publication",
            extracted_text="The continents are fixed in place. The Earth's crust moves primarily vertically due to thermal contraction and geosynclinal development."
        ),
        EpistemicEvidence(
            source_id="EV_PT_RIDGES",
            source_type="Publication",
            extracted_text="Sonar mapping reveals massive mid-ocean ridges stretching across the globe. High heat flow is measured at the crest of these ridges."
        ),
        EpistemicEvidence(
            source_id="EV_PT_MAGNETIC",
            source_type="Publication",
            extracted_text="Oceanographic surveys show strange, zebra-like patterns of magnetic anomalies (alternating high and low magnetic intensities) on the seafloor parallel to the mid-ocean ridges."
        ),
        EpistemicEvidence(
            source_id="EV_PT_WAGENER",
            source_type="Publication",
            extracted_text="Alfred Wegener's 'continental drift' hypothesis is widely rejected because there is no known physical mechanism that could force solid continents through the solid oceanic crust."
        )
    ],
    hidden_outcome="The seafloor is spreading. New crust is formed at mid-ocean ridges and records the Earth's magnetic field reversals as it moves outward, validating continental drift via plate tectonics.",
    constraints=[
        "Magnetic anomaly stripes are symmetric about the mid-ocean ridge axis",
        "Heat flow is highest at ridge crests and decreases with distance",
        "No known mechanism can force solid continents through solid oceanic crust",
        "Continental coastlines (Africa, South America) show geometric fit",
    ],
    candidate_experiments=[
        "Investigate the mid-ocean ridges as massive, static volcanic extrusions caused by localized mantle hotspots.",
        "Model the magnetic anomalies as alternating bands of different rock types (basalt vs. gabbro) with naturally differing magnetic susceptibilities.",
        "Propose that the magnetic stripes record the Earth's magnetic field reversals on newly formed crust moving laterally away from the ridge crests, and test this by dating the rocks.",
        "Attempt to prove the expanding Earth hypothesis, suggesting the ridges are stretch marks from the Earth growing in radius over time."
    ],
    historical_winner="Propose that the magnetic stripes record the Earth's magnetic field reversals on newly formed crust moving laterally away from the ridge crests, and test this by dating the rocks.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Consensus-reversal"
)
