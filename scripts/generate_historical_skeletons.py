import os

cases = [
    ("case_h_pylori", "Medicine", "HRC_H_PYLORI"),
    ("case_mrna_lnp", "Drug delivery", "HRC_MRNA_LNP"),
    ("case_plate_tectonics", "Geology", "HRC_PLATE_TECTONICS"),
    ("case_prions", "Neuroscience", "HRC_PRIONS"),
    ("case_quasicrystals", "Materials science", "HRC_QUASICRYSTALS"),
    ("case_ht_superconductors", "Physics", "HRC_HT_SUPERCONDUCTORS"),
    ("case_rnai", "Molecular biology", "HRC_RNAI"),
    ("case_helicase", "Biochemistry", "HRC_HELICASE"),
    ("case_gravitational_waves", "Physics", "HRC_GRAVITATIONAL_WAVES")
]

template = """from aidp.evaluation.schemas import HistoricalReplayCase

case_data = HistoricalReplayCase(
    case_id="{case_id}",
    domain="{domain}",
    time_window="YYYY-YYYY",
    known_evidence=[],
    hidden_outcome="[Pending Literature Review]",
    candidate_experiments=[
        "[Pending Candidate 1]",
        "[Pending Candidate 2]",
        "[Historical Winner Placeholder]"
    ],
    historical_winner="[Historical Winner Placeholder]",
    evaluation_metric="Percentile Rank",
    difficulty_rating="[Easy/Medium/Hard/Paradigm-shift]"
)
"""

base_dir = os.path.join("tests", "evaluation", "datasets", "historical_cases")
os.makedirs(base_dir, exist_ok=True)

# Also create an __init__.py that imports all cases
init_lines = []

for filename, domain, case_id in cases:
    filepath = os.path.join(base_dir, f"{filename}.py")
    with open(filepath, "w") as f:
        f.write(template.format(case_id=case_id, domain=domain))
    init_lines.append(f"from .{filename} import case_data as {filename}")

init_lines.append("from .case_crispr import case_crispr")

init_filepath = os.path.join(base_dir, "__init__.py")
with open(init_filepath, "w") as f:
    f.write("\n".join(init_lines))
    f.write("\n\nALL_CASES = [\n")
    for filename, _, _ in cases:
        f.write(f"    {filename},\n")
    f.write("    case_crispr\n]\n")

print("Created 9 skeleton cases and __init__.py.")
