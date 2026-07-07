from aidp.meta_learning.simulator import DiscoverySimulator


def test_discovery_simulator() -> None:
    simulator = DiscoverySimulator()
    metrics = simulator.run_benchmark(start_year=2020, end_year=2023, target_domain="Oncology")

    assert "predictive_accuracy" in metrics
    assert "average_novelty" in metrics
    assert "cost_efficiency" in metrics
