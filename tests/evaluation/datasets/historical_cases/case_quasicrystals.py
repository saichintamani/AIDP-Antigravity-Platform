from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_QUASICRYSTALS",
    domain="Crystallography / Condensed Matter Physics",
    time_window="Cutoff Date: April 7, 1982",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_CRYSTAL_RESTRICTION",
            source_type="Publication",
            extracted_text="The Crystallographic Restriction Theorem dictates that crystals must possess translational periodicity. Therefore, 5-fold and 10-fold symmetries are mathematically impossible."
        ),
        EpistemicEvidence(
            source_id="EV_ELECTRON_DIFFRACTION",
            source_type="Publication",
            extracted_text="Electron diffraction patterns of the Aluminum-Manganese alloy display sharp spots, which traditionally indicate a highly ordered, crystalline solid rather than an amorphous glass."
        ),
        EpistemicEvidence(
            source_id="EV_MULTIPLE_TWINNING",
            source_type="Publication",
            extracted_text="Certain crystalline defects known as 'multiple twinning' can overlap to produce diffraction patterns that mimic forbidden symmetries, though they are just standard periodic micro-crystals bound together."
        )
    ],
    constraints=[
        "Mathematical proof: Any proposed structural model must account for the strict mathematical impossibility of 5-fold and 10-fold translational periodicity in 3D space.",
        "Physical evidence: The model must explain the presence of sharp diffraction spots, which absolutely requires long-range structural order.",
        "Parsimony: The model should ideally avoid invoking complex, highly improbable micro-twinning boundary arrangements if a simpler explanation exists."
    ],
    candidate_experiments=[
        # Candidate A (Instrument Artifact)
        "Treat the pattern as an instrumental artifact of the electron microscope's astigmatism. Recalibrate the magnetic lenses, align the beam, and repeat the diffraction on a standard calibration sample.",
        
        # Candidate B (Historical Consensus - Multiple Twinning)
        "Assume the 10-fold symmetry is an illusion caused by multiple twinning of standard periodic crystals. Focus on high-resolution dark-field microscopy to locate the microscopic twin boundaries and confirm the material is composed of ordinary micro-crystals.",
        
        # Candidate C (Historical Winner)
        "Accept the non-crystallographic 10-fold symmetry with sharp diffraction spots as a genuine, novel physical state (a quasi-periodic crystal). Derive a mathematical projection from a higher-dimensional space (e.g., 6D to 3D) to explain how sharp diffraction can occur without periodic translation.",
        
        # Candidate D (Material Contamination)
        "Discard the sample as defective. Assume the rapid cooling process introduced impurities or oxidation. Synthesize a new batch of Aluminum-Manganese alloy with stricter atmospheric controls and slower cooling rates to achieve a standard crystalline phase."
    ],
    historical_winner="Accept the non-crystallographic 10-fold symmetry with sharp diffraction spots as a genuine, novel physical state (a quasi-periodic crystal). Derive a mathematical projection from a higher-dimensional space (e.g., 6D to 3D) to explain how sharp diffraction can occur without periodic translation.",
    hidden_outcome="The alloy demonstrated true quasi-periodicity. Shechtman's discovery was initially met with severe backlash and mockery from figures like Linus Pauling, but it fundamentally overturned the definition of a crystal, earning the Nobel Prize in 2011.",

    evaluation_metric="Percentile Rank",
    difficulty_rating="Consensus-reversal"
)
