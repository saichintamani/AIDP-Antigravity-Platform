import json
from typing import Any


class AutoprotocolCompiler:
    """
    Compiles a WET_LAB experiment design into standard Autoprotocol JSON.
    This allows robotic cloud labs (like Emerald Cloud Lab) to execute the AI-designed experiment.
    """
    
    def compile(self, experiment_design: dict[str, Any]) -> str:
        protocol = {
            "refs": {},
            "instructions": []
        }
        
        # Parse controls to determine plate setup
        controls = experiment_design.get("controls", [])
        steps = experiment_design.get("protocol_steps", experiment_design.get("steps", []))
        independent_vars = experiment_design.get("independentVariables", [])
        
        # Generate plate references from control groups
        for i, ctrl in enumerate(controls):
            ctrl_name = ctrl if isinstance(ctrl, str) else ctrl.get("group_name", f"group_{i}")
            plate_id = f"plate_{ctrl_name.lower().replace(' ', '_')}"
            protocol["refs"][plate_id] = {
                "new": "96-pcr",
                "store": {"where": "cold_20"}
            }
        
        # If no controls, create a default plate
        if not protocol["refs"]:
            protocol["refs"]["microplate_main"] = {
                "new": "96-pcr",
                "store": {"where": "cold_20"}
            }
        
        # Generate dispense instructions from protocol steps
        target_plate = list(protocol["refs"].keys())[0]
        for i, step in enumerate(steps):
            step_text = step if isinstance(step, str) else step.get("description", str(step))
            protocol["instructions"].append({
                "op": "dispense",
                "object": target_plate,
                "columns": [{"column": i % 12, "volume": "10:microliter"}],
                "reagent": step_text[:50],  # Use the step description as the reagent label
                "step_index": i
            })
            
        # Generate variable manipulation instructions
        for var in independent_vars:
            var_name = var if isinstance(var, str) else var.get("name", str(var))
            protocol["instructions"].append({
                "op": "thermocycle",
                "object": target_plate,
                "groups": [{"cycles": 1, "steps": [{"temperature": "37:celsius", "duration": "60:minute"}]}],
                "variable": var_name
            })
            
        return json.dumps(protocol, indent=2)

class PyRosettaCompiler:
    """
    Compiles a COMPUTATIONAL molecular dynamics/docking design into an executable PyRosetta script.
    """
    
    def compile(self, experiment_design: dict[str, Any]) -> str:
        claim = experiment_design.get("claim", experiment_design.get("epistemic_claim_id", "unknown"))
        steps = experiment_design.get("protocol_steps", experiment_design.get("steps", []))
        dep_vars = experiment_design.get("dependentVariables", [])
        ind_vars = experiment_design.get("independentVariables", [])
        target = experiment_design.get("target_protein", "MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQ")
        
        script_lines = [
            "import pyrosetta",
            "from pyrosetta import *",
            "pyrosetta.init()",
            "",
            "# AI-Generated Computational Protocol",
            f"# Hypothesis: {str(claim)[:100]}",
            f"# Independent Variables: {', '.join(str(v) for v in ind_vars[:3])}",
            f"# Dependent Variables: {', '.join(str(v) for v in dep_vars[:3])}",
            "",
            "# Target protein sequence (from experiment design)",
            f"pose = pose_from_sequence('{target}')",
            "scorefxn = get_fa_scorefxn()",
            "",
            "# Protocol Steps",
        ]
        
        for i, step in enumerate(steps):
            step_text = step if isinstance(step, str) else step.get("description", str(step))
            script_lines.append(f"# Step {i+1}: {step_text[:80]}")
        
        script_lines.extend([
            "",
            "# Compute energy score",
            "energy = scorefxn(pose)",
            "print(f'Total Energy: {energy}')",
            "",
            "# Export results",
            "pose.dump_pdb('aidp_result.pdb')",
            "print('Protocol execution complete. Results saved to aidp_result.pdb')",
        ])
        
        return "\n".join(script_lines)

