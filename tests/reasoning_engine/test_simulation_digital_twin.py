from aidp.reasoning_engine.digital_twin import DigitalTwinLaboratory
from aidp.reasoning_engine.simulation_engine import SimulationEngine


def test_digital_twin_simulation() -> None:
    engine = SimulationEngine()
    twin = DigitalTwinLaboratory(engine)

    # High power design reduces entropy -> high EIG
    high_power_design = {"power": 0.9}
    res_high = twin.simulate_experiment(high_power_design)

    # Low power design leaves high entropy -> low EIG
    low_power_design = {"power": 0.5}
    res_low = twin.simulate_experiment(low_power_design)

    assert res_high.expected_information_gain > res_low.expected_information_gain
    assert res_high.risk_of_failure < res_low.risk_of_failure
