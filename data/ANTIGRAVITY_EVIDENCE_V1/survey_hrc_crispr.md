# Expert Evaluation Survey: Molecular Biology & Gene Editing Breakthrough

**Case ID:** HRC_CRISPR
**Historical Time Window:** Up to 2010-2012
**Difficulty Rating:** Paradigm-shift

## Instructions
You are acting as a peer-reviewer evaluating grant proposals or experimental directions at the cutoff date specified above. You MUST NOT use any knowledge discovered after this date. 

Based **strictly on the evidence provided below**, please rank the candidate experiments from 1 (Most likely to lead to a breakthrough) to 4 (Least likely).

---

## 1. Available Evidence

### EV_CRISPR_DUAL_RNA (Publication)
> Biochemical isolation of the Cas9 complex reveals that it strictly requires TWO separate RNA molecules to function: a CRISPR RNA (crRNA) that contains the 20-nucleotide targeting sequence, and a trans-activating CRISPR RNA (tracrRNA) that forms a structural scaffold to lock into Cas9.

- **Tags:** Biochemistry, crRNA, tracrRNA
- **Entity Relationships:** Cas9_Activation -> requires -> (crRNA AND tracrRNA)

### EV_CRISPR_CLEAVAGE_DOMAINS (Publication)
> Cas9 utilizes two distinct nuclease domains: the HNH domain cleaves the DNA strand complementary to the crRNA guide, while the RuvC-like domain cleaves the non-complementary DNA strand.

- **Tags:** Structural_Biology, HNH_Domain, RuvC_Domain, Endonuclease

### EV_CRISPR_RNA_BASEPAIRING (Publication)
> The crRNA and tracrRNA interact via a short stretch of complementary base-pairing to form a stable duplex. Structural modeling indicates the 3' end of the crRNA and the 5' end of the tracrRNA are approximately 40 Ångströms apart.

- **Tags:** Structural_Biology, RNA_Duplex, Distance_Constraints
- **Mathematical Constraints:** Distance(3_prime_crRNA, 5_prime_tracrRNA) ~= 40_Angstroms

### Explicit Scientific Constraints
- Cas9 requires BOTH crRNA AND tracrRNA simultaneously to function
- Distance(3_prime_crRNA, 5_prime_tracrRNA) ~= 40 Angstroms
- HNH domain cleaves complementary strand; RuvC cleaves non-complementary strand
- Any linker must preserve the crRNA:tracrRNA duplex secondary structure

---

## 2. Candidate Experiments to Rank

**Option A:**
Attempt to deliver Cas9 protein along with separate crRNA and tracrRNA transcripts into mammalian cells, relying on spontaneous self-assembly.

**Option B:**
Engineer the Cas9 protein to directly bind double-stranded DNA without needing any RNA guides, to simplify the system for gene editing.

**Option C:**
Covalently link the 3' end of the crRNA to the 5' end of the tracrRNA using a synthetic GAAA tetraloop to bridge the 40 Å gap, creating a Single-Guide RNA (sgRNA) that programs Cas9 cleavage.

**Option D:**
Mutate the tracrRNA sequence to make it universally bind to any host genomic DNA, turning Cas9 into a random mutagen.

---

## 3. Your Ranking & Rationale

**Top Choice (Rank 1):** Option [ ]
**Rank 2:** Option [ ]
**Rank 3:** Option [ ]
**Rank 4:** Option [ ]

**Rationale for Top Choice (Max 150 words):**



