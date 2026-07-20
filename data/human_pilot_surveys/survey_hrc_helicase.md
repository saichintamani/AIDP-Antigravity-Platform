# Expert Evaluation Survey: Biochemistry Breakthrough

**Case ID:** HRC_HELICASE
**Historical Time Window:** Up to 1970-1979
**Difficulty Rating:** Paradigm-shift

## Instructions
You are acting as a peer-reviewer evaluating grant proposals or experimental directions at the cutoff date specified above. You MUST NOT use any knowledge discovered after this date. 

Based **strictly on the evidence provided below**, please rank the candidate experiments from 1 (Most likely to lead to a breakthrough) to 4 (Least likely).

---

## 1. Available Evidence

### EV_HELICASE_THERMODYNAMICS (Publication)
> The hydrogen bonds holding the DNA duplex together are highly stable; spontaneous unwinding at physiological temperatures is thermodynamically forbidden, especially ahead of a replication fork moving at 1000 base pairs per second.

- **Tags:** Biophysics, Thermodynamics, Replication_Fork
- **Mathematical Constraints:** Delta_G_melting(37C) > 0, Fork_Speed == 1000_bp/sec

### EV_HELICASE_ATP_REQUIREMENT (Publication)
> In vitro DNA replication assays have demonstrated an absolute requirement for ATP hydrolysis, even when the polymerase itself does not consume ATP for polymerization. The Rep protein exhibits single-stranded DNA-dependent ATPase activity, yielding -30.5 kJ/mol.

- **Tags:** Enzymology, In_Vitro_Assays, ATP_Hydrolysis
- **Mathematical Constraints:** Delta_G(ATP_Hydrolysis) == -30.5_kJ/mol, Replication_Rate(ATP_depleted) == 0

### EV_HELICASE_REP_MUTANT (Publication)
> Certain E. coli mutants (rep) are severely defective in DNA replication but possess fully functional DNA polymerases and ligases.

- **Tags:** Genetics, Microbiology, Mutagenesis
- **Entity Relationships:** rep_Gene_Mutation -> impairs -> DNA_Replication, DNA_Polymerase -> is_functional_in -> rep_Mutant

### EV_HELICASE_DIMER_ROTATION (Publication)
> Structural predictions suggest that a functional unwinding motor would likely operate as an oligomer, undergoing massive conformational changes powered by ATP to continuously translocate on DNA.

- **Tags:** Structural_Biology, Protein_Dynamics, Conformational_Change
- **Mathematical Constraints:** Oligomeric_State >= 2

### Explicit Scientific Constraints
- Separation of DNA strands must couple with ATP hydrolysis
- Separation rate must be significantly faster than thermal breathing alone
- Enzyme must act actively, not passively waiting for fluctuations

---

## 2. Candidate Experiments to Rank

**Option A:**
Purify the rep protein and demonstrate that it acts as a dedicated molecular motor, coupling the hydrolysis of ATP directly to the active mechanical separation of the DNA double helix.

**Option B:**
Propose that DNA polymerase itself physically forces the strands apart as it moves forward, requiring no independent unwinding enzyme, and utilizing the energy of dNTP incorporation.

**Option C:**
Assume DNA strands spontaneously 'breathe' open due to thermal fluctuations at physiological temperatures, allowing SSBs to passively trap the single strands, and measure binding kinetics.

**Option D:**
Investigate if the Rep protein simply degrades the complementary DNA strand entirely to allow the polymerase to easily copy the remaining single strand without needing unwinding.

---

## 3. Your Ranking & Rationale

**Top Choice (Rank 1):** Option [ ]
**Rank 2:** Option [ ]
**Rank 3:** Option [ ]
**Rank 4:** Option [ ]

**Rationale for Top Choice (Max 150 words):**



