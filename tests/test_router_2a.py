from aidp.discovery.domain_routing import DomainDetector, DomainRouter, ScientificDomain


class MockPlanner:
    def __init__(self, expected_domain_str: str):
        self.expected_domain_str = expected_domain_str

    def execute_task(self, spec):
        return {"domain": self.expected_domain_str}

def test_domain_detector():
    # Test Wet Lab
    detector = DomainDetector(planner=MockPlanner("WET_LAB"))
    domain = detector.detect_domain("CRISPR screen identifies targets", "query")
    assert domain == ScientificDomain.WET_LAB
    
    # Test Clinical Trial
    detector = DomainDetector(planner=MockPlanner("CLINICAL_TRIAL"))
    domain = detector.detect_domain("Phase III efficacy", "query")
    assert domain == ScientificDomain.CLINICAL_TRIAL
    
    # Test Computational
    detector = DomainDetector(planner=MockPlanner("COMPUTATIONAL"))
    domain = detector.detect_domain("MD simulation of binding pocket", "query")
    assert domain == ScientificDomain.COMPUTATIONAL
    
    # Test Fallback
    detector = DomainDetector(planner=MockPlanner("CLINICAL_TRIAL_RANDOM_TEXT"))
    domain = detector.detect_domain("clinical patient cohort", "query")
    assert domain == ScientificDomain.CLINICAL_TRIAL

def test_domain_router():
    class MockGateway:
        def query(self, *args, **kwargs):
            return None
    
    router = DomainRouter(gateway=MockGateway())
    
    planner = router.get_planner(ScientificDomain.COMPUTATIONAL)
    from aidp.discovery.computational_planning import ComputationalPlanner
    assert isinstance(planner, ComputationalPlanner)

if __name__ == "__main__":
    test_domain_detector()
    test_domain_router()
    print("Compartment 2A tests passed.")
