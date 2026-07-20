from aidp.evaluation.schemas import HistoricalReplayCase
from aidp.intelligence.epistemic_models import EpistemicEvidence

case_data = HistoricalReplayCase(
    case_id="HRC_MRNA_LNP",
    domain="Drug Delivery & Immunology",
    time_window="1995-2005",
    known_evidence=[
        EpistemicEvidence(
            source_id="EV_MRNA_TLR_ACTIVATION",
            source_type="Publication",
            extracted_text="In vitro transcribed (IVT) mRNA is highly immunogenic. It does not activate TLR7/8 directly; instead, it is cleaved by RNase T2 in the endolysosome into short immunostimulatory fragments that fit the TLR7/8 binding pocket.",
            ontology_tags=["Immunology", "Toll_Like_Receptors", "RNase_T2"],
            entity_relationships=["IVT_mRNA -> cleaved_by -> RNase_T2 -> activates -> TLR7/8"]
        ),
        EpistemicEvidence(
            source_id="EV_MRNA_PSEUDOURIDINE",
            source_type="Publication",
            extracted_text="Mammalian cellular RNA contains naturally occurring modified nucleosides. Substituting Uridine with Pseudouridine (Ψ) alters the RNA's conformational flexibility, making it sterically resistant to RNase T2 cleavage.",
            ontology_tags=["Biochemistry", "Pseudouridine", "Enzyme_Kinetics"],
            mathematical_constraints=["Cleavage_Rate(Pseudouridine, RNase_T2) ~= 0"]
        ),
        EpistemicEvidence(
            source_id="EV_MRNA_RNASE_BARRIER",
            source_type="Publication",
            extracted_text="Human blood is saturated with endogenous RNases. Unprotected mRNA injected intravenously is enzymatically degraded within seconds, yielding a half-life near zero.",
            ontology_tags=["Biochemistry", "RNase", "Pharmacokinetics"],
            mathematical_constraints=["Half_Life(Naked_mRNA, Blood) < 10_seconds"]
        ),
        EpistemicEvidence(
            source_id="EV_LNP_IONIZATION_PHASE",
            source_type="Publication",
            extracted_text="Positively charged lipids are highly toxic in vivo. However, lipids with a pKa of 6.2-6.5 remain neutral at physiological pH (7.4). At endosomal pH (5.5), they protonate and interact with anionic endosomal lipids, triggering a phase transition from a stable lamellar bilayer into an unstable inverse hexagonal (HII) phase, which ruptures the membrane.",
            ontology_tags=["Physical_Chemistry", "Lipid_Nanoparticles", "Inverse_Hexagonal_Phase", "pKa"],
            mathematical_constraints=[
                "pKa(Lipid) == 6.2_to_6.5",
                "Phase(Lipid, pH_7.4) == Lamellar",
                "Phase(Lipid, pH_5.5) == Inverse_Hexagonal_HII"
            ]
        )
    ],
    hidden_outcome="The successful therapeutic application of mRNA requires a dual breakthrough: substituting Uridine with Pseudouridine to prevent RNase T2 cleavage (evading TLRs), and encapsulating the mRNA in an Ionizable LNP with a pKa of 6.2-6.5 to trigger an HII phase transition for endosomal escape.",
    constraints=[
        "mRNA must evade TLR activation (immune response)",
        "Delivery vehicle must protect mRNA from extracellular RNases",
        "Delivery vehicle must enable endosomal escape into the cytosol",
        "Delivery vehicle pKa must be between 6.2 and 6.5 for targeted release",
    ],
    candidate_experiments=[
        "Develop stronger immunosuppressive drugs to block the cytokine storm, hoping naked mRNA enters cells before RNase degradation.",
        "Synthesize IVT mRNA using pseudouridine to block RNase T2 cleavage, and encapsulate it in an ionizable lipid nanoparticle (pKa 6.2-6.5) to trigger HII phase-mediated endosomal escape.",
        "Engineer the mRNA sequence to remove all putative secondary structures, and deliver it using a permanently cationic liposome.",
        "Abandon non-viral mRNA and focus exclusively on improving adeno-associated viral (AAV) vectors for safer delivery."
    ],
    historical_winner="Synthesize IVT mRNA using pseudouridine to block RNase T2 cleavage, and encapsulate it in an ionizable lipid nanoparticle (pKa 6.2-6.5) to trigger HII phase-mediated endosomal escape.",
    evaluation_metric="Percentile Rank",
    difficulty_rating="Paradigm-shift"
)
