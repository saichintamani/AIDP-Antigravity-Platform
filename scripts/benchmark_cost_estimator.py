import yaml
from pathlib import Path

# Static cost estimates per 1M tokens
COST_MATRIX = {
    "gpt-4-turbo": {"input": 10.0, "output": 30.0},
    "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
    "gpt-4o": {"input": 5.0, "output": 15.0}
}

# Average token consumption estimates per case (input, output)
CASE_ESTIMATES = {
    "Baseline A": (1000, 500),
    "Baseline B": (5000, 1000),  # Includes context injection
    "Baseline C": (15000, 4000)  # Multi-agent debate and reasoning loops
}

def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def estimate_cost(config: dict, num_cases: int = 20):
    print("--- Benchmark Cost Forecaster ---")
    
    models = {
        "Baseline A": config["models"]["baseline_a"]["primary"],
        "Baseline B": config["models"]["baseline_b"]["primary"],
        "Baseline C": config["models"]["baseline_c_aidp"]["reasoning_model"]
    }
    
    total_cost = 0.0
    
    for baseline, model in models.items():
        if model not in COST_MATRIX:
            print(f"Warning: Model {model} not in cost matrix. Assuming gpt-4-turbo costs.")
            model = "gpt-4-turbo"
            
        in_cost_per_m = COST_MATRIX[model]["input"]
        out_cost_per_m = COST_MATRIX[model]["output"]
        
        in_tokens, out_tokens = CASE_ESTIMATES[baseline]
        
        cost_per_case = (in_tokens / 1_000_000 * in_cost_per_m) + (out_tokens / 1_000_000 * out_cost_per_m)
        baseline_total = cost_per_case * num_cases
        total_cost += baseline_total
        
        print(f"{baseline} ({model}):")
        print(f"  Cost per case: ${cost_per_case:.4f}")
        print(f"  Total for {num_cases} cases: ${baseline_total:.4f}")
        
    print("-" * 33)
    print(f"Estimated Total Full Benchmark Cost: ${total_cost:.2f}")
    
    budget_cap = config.get("live_execution", {}).get("budget_cap_usd", 0.0)
    if total_cost > budget_cap:
        print(f"WARNING: Estimated cost (${total_cost:.2f}) exceeds configured budget cap (${budget_cap:.2f})!")

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    config_path = base_dir / "benchmark_execution_config.yaml"
    config = load_config(str(config_path))
    estimate_cost(config, num_cases=20)
