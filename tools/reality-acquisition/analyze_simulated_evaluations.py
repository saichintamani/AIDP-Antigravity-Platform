import json
import statistics
from pathlib import Path
from collections import defaultdict

RESULTS_FILE = Path("data/human_pilot_surveys/simulated_evaluations.json")
OUTPUT_REPORT = Path("data/human_pilot_surveys/SIMULATION_REPORT.md")

def analyze_results():
    if not RESULTS_FILE.exists():
        print(f"File not found: {RESULTS_FILE}")
        return

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Aggregates
    track_scores = defaultdict(lambda: defaultdict(list))
    persona_scores = defaultdict(lambda: defaultdict(list))
    case_scores = defaultdict(lambda: defaultdict(list))

    for entry in data:
        track = entry["track"]
        persona = entry["persona"]
        case = entry["case"]
        scores = entry["scores"]

        for dim in ["leakage_resistance", "reasoning_depth", "constraint_compliance", "scientific_usefulness"]:
            val = scores.get(dim)
            if val is not None:
                track_scores[track][dim].append(val)
                persona_scores[persona][dim].append(val)
                case_scores[case][dim].append(val)

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("# Simulated Human Evaluation Report\n\n")
        f.write("## 1. Do domain experts detect hidden flaws/leakage?\n")
        f.write(f"- Clean Track (A1) avg Leakage Resistance: {avg(track_scores['Track_A1']['leakage_resistance']):.2f}/10\n")
        f.write(f"- Contaminated Track (A2) avg Leakage Resistance: {avg(track_scores['Track_A2']['leakage_resistance']):.2f}/10\n")
        f.write("> **Analysis**: The difference in scores indicates the degree to which evaluators noticed the historical leakage in Track A2.\n\n")
        
        f.write("## 2. Do they score Contaminated (Track A2) higher on usefulness despite leakage?\n")
        f.write(f"- Clean Track (A1) avg Usefulness: {avg(track_scores['Track_A1']['scientific_usefulness']):.2f}/10\n")
        f.write(f"- Contaminated Track (A2) avg Usefulness: {avg(track_scores['Track_A2']['scientific_usefulness']):.2f}/10\n")
        f.write("> **Analysis**: If Track A2 usefulness is higher, it means the 'cheating' made the answer seem more scientifically useful to the evaluators, masking the lack of constraint compliance.\n\n")

        f.write("## 3. Are there calibration differences across personas?\n")
        for persona, dims in persona_scores.items():
            f.write(f"### {persona}\n")
            f.write(f"- Leakage Resistance: {avg(dims['leakage_resistance']):.2f}\n")
            f.write(f"- Reasoning Depth: {avg(dims['reasoning_depth']):.2f}\n")
            f.write(f"- Constraint Compliance: {avg(dims['constraint_compliance']):.2f}\n")
            f.write(f"- Scientific Usefulness: {avg(dims['scientific_usefulness']):.2f}\n\n")

        f.write("## 4. Do they disagree with each other (Variance)?\n")
        for dim in ["leakage_resistance", "reasoning_depth", "constraint_compliance", "scientific_usefulness"]:
            all_scores = track_scores["Track_A1"][dim] + track_scores["Track_A2"][dim]
            var = statistics.variance(all_scores) if len(all_scores) > 1 else 0
            f.write(f"- **{dim}** Variance across all evaluations: {var:.2f}\n")
        
        f.write("\n## 5. Raw Persona Notes\n")
        # Print a few rationales for Prions or Quasicrystals
        f.write("### Sample Rationales for Prions/Quasicrystals\n")
        for entry in data:
            if "prion" in entry["case"].lower() or "quasicrystal" in entry["case"].lower():
                f.write(f"- **[{entry['track']} - {entry['case']}] {entry['persona']}**: {entry['scores'].get('rationale', 'N/A')}\n")

    print(f"Report generated at {OUTPUT_REPORT}")

if __name__ == "__main__":
    analyze_results()
