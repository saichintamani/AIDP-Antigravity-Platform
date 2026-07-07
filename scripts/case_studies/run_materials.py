from aidp.evaluation.suite import ScientificEvaluationSuite

def run_materials_case_study():
    """
    Simulates a full unmocked campaign for discovering solid-state battery electrolytes.
    """
    print("Starting Materials Science Case Study: Solid-State Electrolytes...")
    
    suite = ScientificEvaluationSuite()
    metrics = suite.evaluate_campaign_mock(domain="Materials")
    
    print("Campaign Complete.")
    print(f"Metrics: {metrics}")

if __name__ == "__main__":
    run_materials_case_study()
