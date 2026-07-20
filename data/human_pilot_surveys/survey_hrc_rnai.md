# Expert Evaluation Survey: Molecular Biology Breakthrough

**Case ID:** HRC_RNAI
**Historical Time Window:** Up to 1990-1998
**Difficulty Rating:** Paradigm-shift

## Instructions
You are acting as a peer-reviewer evaluating grant proposals or experimental directions at the cutoff date specified above. You MUST NOT use any knowledge discovered after this date. 

Based **strictly on the evidence provided below**, please rank the candidate experiments from 1 (Most likely to lead to a breakthrough) to 4 (Least likely).

---

## 1. Available Evidence

### EV_RNAI_ANTISENSE (Publication)
> Antisense RNA (single-stranded RNA complementary to an mRNA) is known to inhibit gene expression by stoichiometrically binding the mRNA and preventing translation via 1:1 steric hindrance.

- **Tags:** Molecular_Biology, Gene_Silencing, Antisense_Therapy
- **Mathematical Constraints:** Silencing_Ratio(Antisense_RNA, mRNA) == 1:1
- **Entity Relationships:** Antisense_RNA -> inhibits -> Translation

### EV_RNAI_COSUPPRESSION (Publication)
> In petunias, introducing extra copies of a chalcone synthase gene paradoxically suppresses both the endogenous gene and the introduced gene, causing white flowers. This is termed 'cosuppression' (Napoli et al. 1990).

- **Tags:** Genetics, Botany, Epigenetics, Cosuppression
- **Mathematical Constraints:** Expression_Level(Transgene + Endogenous) == 0
- **Entity Relationships:** Transgene -> suppresses -> Endogenous_Gene

### EV_RNAI_NEMATODE_ANOMALY (Publication)
> In C. elegans, injecting 'sense' par-1 RNA (identical to mRNA) surprisingly causes the same silencing effect as injecting 'antisense' RNA (Guo & Kemphues 1995).

- **Tags:** Molecular_Biology, Nematology, Experimental_Anomaly
- **Mathematical Constraints:** Silencing_Effect(Sense_RNA) == Silencing_Effect(Antisense_RNA)

### EV_RNAI_PREPARATIONS (Publication)
> RNA preparations synthesized in vitro often contain trace amounts of double-stranded RNA (dsRNA) as a byproduct of the T7 polymerase reaction.

- **Tags:** Biochemistry, In_Vitro_Transcription, Contaminants
- **Entity Relationships:** T7_Polymerase -> produces -> dsRNA_Byproduct

### Explicit Scientific Constraints
- Silencing must be sub-stoichiometric (a few molecules silence abundant mRNA)
- Sense and antisense RNA individually are inefficient; they must act together
- The trigger must be highly specific to the target sequence

---

## 2. Candidate Experiments to Rank

**Option A:**
Hypothesize that 'sense' RNA injections act as a sponge for naturally occurring endogenous antisense RNA, disrupting a natural homeostatic equilibrium, and test this by measuring endogenous antisense levels.

**Option B:**
Test highly purified double-stranded RNA (dsRNA) against highly purified single-stranded RNA, hypothesizing that trace dsRNA is the true, highly potent trigger for gene silencing acting via a sub-stoichiometric (catalytic) destruction of mRNA.

**Option C:**
Propose that cosuppression and sense-silencing are caused by transcriptional silencing via DNA methylation triggered by high concentrations of ectopic RNA molecules targeting the promoter.

**Option D:**
Investigate whether the introduction of any foreign RNA simply over-activates a generic antiviral ribonuclease (RNase L) that indiscriminately degrades all mRNA in the cytoplasm.

---

## 3. Your Ranking & Rationale

**Top Choice (Rank 1):** Option [ ]
**Rank 2:** Option [ ]
**Rank 3:** Option [ ]
**Rank 4:** Option [ ]

**Rationale for Top Choice (Max 150 words):**



