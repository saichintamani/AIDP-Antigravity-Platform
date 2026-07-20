from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_H_PYLORI",
    domain="Medicine",
    time_window="1970-1982",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_HP_CONSENSUS_1",
            source_type="Publication",
            extracted_text="Peptic ulcers are caused by excess gastric acid secretion exacerbated by stress, diet, and lifestyle factors. The stomach is sterile due to its highly acidic environment (pH 1-2)."
        ),
        EpistemicEvidence(
            source_id="EV_HP_OBS_1",
            source_type="Publication",
            extracted_text="Spiral-shaped bacteria are occasionally observed in human gastric mucosa biopsies, but they are widely considered to be post-mortem contaminants or secondary colonizers of already existing lesions."
        ),
        EpistemicEvidence(
            source_id="EV_HP_TREATMENT",
            source_type="Publication",
            extracted_text="Treatment with antacids or H2-receptor antagonists provides temporary relief and ulcer healing, but relapse rates are extraordinarily high (up to 80% within a year) once treatment stops."
        ),
        EpistemicEvidence(
            source_id="EV_HP_BISMUTH",
            source_type="Publication",
            extracted_text="Bismuth salts, which have known antimicrobial properties, sometimes lead to lower ulcer relapse rates compared to standard acid suppression, though the mechanism is unknown."
        )
    ],
    hidden_outcome="Peptic ulcers are primarily caused by infection with the bacterium Helicobacter pylori, not by stress or diet. Eradicating the bacteria cures the disease.",
    constraints=[
        "Stomach pH is 1-2 (highly acidic), any causal pathogen must survive this environment",
        "Ulcer relapse rate is ~80% within 1 year of stopping acid suppression therapy",
        "Bismuth salts (antimicrobial) produce lower relapse rates than pure acid suppression",
        "Spiral bacteria are repeatedly observed in gastric biopsies across multiple patients",
    ],
    candidate_experiments=[
        "Develop stronger and longer-lasting acid suppression drugs (e.g., proton pump inhibitors) to continuously manage the acidic environment.",
        "Conduct large-scale epidemiological studies on the effects of psychological stress reduction and dietary changes on ulcer relapse rates.",
        "Attempt to culture the spiral bacteria from gastric biopsies and administer targeted antibiotic therapy to ulcer patients to observe if relapse rates drop.",
        "Investigate the genetic predisposition to acid hypersecretion in ulcer patients."
    ],
    historical_winner="Attempt to culture the spiral bacteria from gastric biopsies and administer targeted antibiotic therapy to ulcer patients to observe if relapse rates drop.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Paradigm-shift"
)
