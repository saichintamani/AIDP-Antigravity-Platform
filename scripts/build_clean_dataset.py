import json
import os

def clean_dataset():
    # Load original N=10
    n10_path = "data/ANTIGRAVITY_EVIDENCE_V1/llama3.1_n10_raw.json"
    with open(n10_path, "r") as f:
        n10_data = json.load(f)

    # Load quasicrystals hardening
    qc_path = "data/ANTIGRAVITY_EVIDENCE_V1/quasicrystals_hardening_raw.json"
    qc_clean = None
    if os.path.exists(qc_path):
        with open(qc_path, "r") as f:
            qc_data = json.load(f)
            for item in qc_data:
                if item["version"] == "Version_B":
                    qc_clean = item
                    qc_clean["case"] = "Quasicrystals (Hardened)"
                    break

    # Load prions hardening
    pr_path = "data/ANTIGRAVITY_EVIDENCE_V1/prions_hardening_raw.json"
    pr_clean = None
    if os.path.exists(pr_path):
        with open(pr_path, "r") as f:
            pr_data = json.load(f)
            for item in pr_data:
                # Prefer Version_C (strict boundaries)
                if item["version"] == "Version_C":
                    pr_clean = item
                    pr_clean["case"] = "Prions (Hardened)"
                    break

    # Substitute
    clean_data = []
    for item in n10_data:
        if item["case"] == "Quasicrystals" and qc_clean:
            clean_data.append(qc_clean)
        elif item["case"] == "Prions" and pr_clean:
            clean_data.append(pr_clean)
        else:
            clean_data.append(item)

    # Save
    out_path = "data/ANTIGRAVITY_EVIDENCE_V1/llama3.1_n10_clean_for_humans.json"
    with open(out_path, "w") as f:
        json.dump(clean_data, f, indent=4)
    print(f"Cleaned dataset saved to {out_path}")

if __name__ == "__main__":
    clean_dataset()
