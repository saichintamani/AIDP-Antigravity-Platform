from aidp.evaluation.framework import ScientificReportCard


def run_climate_science_demonstration():
    print("Executing Domain Demonstration: Climate Science (Carbon Capture)")
    print("------------------------------------------------------------------")
    print("1. Searching literature for novel MOF (Metal-Organic Framework) structures...")
    print("2. Extracting evidence and updating world model...")
    print("3. Generating hypotheses via Causal Logic...")
    print("4. Debating in Digital Twin (PSRE)...")
    print("5. Generating Research Roadmap...")
    print("------------------------------------------------------------------")
    
    # Generate final report card
    report_card = ScientificReportCard().generate_report_card({"domain": "Climate Science"})
    print("Campaign Complete. Final Report Card:")
    for metric, score in report_card.items():
        print(f"  - {metric}: {score}")

if __name__ == "__main__":
    run_climate_science_demonstration()
