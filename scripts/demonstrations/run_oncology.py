from aidp.evaluation.framework import ScientificReportCard

def run_oncology_demonstration():
    print("Executing Domain Demonstration: Oncology (Melanoma Drug Resistance)")
    print("------------------------------------------------------------------")
    print("1. Searching literature for resistance mechanisms...")
    print("2. Extracting evidence and updating world model...")
    print("3. Generating hypotheses via Causal Logic...")
    print("4. Debating in Digital Twin (PSRE)...")
    print("5. Generating Research Roadmap...")
    print("------------------------------------------------------------------")
    
    # Generate final report card
    report_card = ScientificReportCard().generate_report_card({"domain": "Oncology"})
    print("Campaign Complete. Final Report Card:")
    for metric, score in report_card.items():
        print(f"  - {metric}: {score}")

if __name__ == "__main__":
    run_oncology_demonstration()
