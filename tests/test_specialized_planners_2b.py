from aidp.discovery.computational_planning import ComputationalPlanner
from aidp.planning.metrics import DomainMetricValidator


# Mock Gateway
class MockGateway:
    def __init__(self):
        self.ablation_config = None
        pass
    def generate_response(self, *args, **kwargs):
        # We don't actually call the LLM in this test since the planner has a hardcoded fallback if execute_task fails
        return None
    def query(self, *args, **kwargs):
        return None

def test_computational_planner_and_metrics():
    gateway = MockGateway()
    planner = ComputationalPlanner(gateway)
    
    hypothesis = {"claim": "Molecular dynamics shows binding affinity"}
    knowledge_context = {}
    
    design = planner.design_experiment(hypothesis, None, knowledge_context)
    
    assert design["domain"] == "COMPUTATIONAL"
    assert "methodology" in design
    assert "hardware" in design["methodology"]
    assert "data_splits" in design["methodology"]
    
    # Now run it through the validator
    validator = DomainMetricValidator()
    result = validator.validate_design(design)
    
    assert result["valid"]
    assert len(result["penalties"]) == 0
    
    # Tamper with the design to trigger a penalty
    del design["methodology"]["data_splits"]["training_set"]
    failed_result = validator.validate_design(design)
    
    assert not failed_result["valid"]
    assert "FATAL" in failed_result["penalties"][0]

if __name__ == "__main__":
    test_computational_planner_and_metrics()
    print("Compartment 2B and 2C tests passed.")
