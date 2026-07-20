import json
import sys
from aidp.intelligence.compilers import AutoprotocolCompiler, PyRosettaCompiler
from aidp.discovery.workflow import DiscoverySession, ExecutionNode, DiscoveryState

def run_tests():
    print("--- Testing AutoprotocolCompiler ---")
    compiler = AutoprotocolCompiler()
    mock_design = {
        "steps": [],
        "controls": ["negative_control"],
        "epistemic_claim_id": "test-claim-123"
    }
    
    result = compiler.compile(mock_design)
    print(result)
    
    print("\n--- Testing PyRosettaCompiler ---")
    compiler2 = PyRosettaCompiler()
    result2 = compiler2.compile(mock_design)
    print(result2)

    print("\n--- Testing ExecutionNode ---")
    session = DiscoverySession()
    session.experiment_design = mock_design
    session.telemetry["domain"] = "WET_LAB"
    
    node = ExecutionNode()
    state = node.execute(session)
    
    print(f"Node returned state: {state}")
    print("Telemetry extracted Autoprotocol payload:")
    print(session.telemetry.get("compiled_autoprotocol"))
    
    session.telemetry["domain"] = "COMPUTATIONAL"
    state = node.execute(session)
    print("Telemetry extracted PyRosetta payload:")
    print(session.telemetry.get("compiled_pyrosetta"))

if __name__ == "__main__":
    run_tests()
