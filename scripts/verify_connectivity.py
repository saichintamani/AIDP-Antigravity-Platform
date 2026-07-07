import os
import time
import json
from pathlib import Path
from datetime import datetime

try:
    import litellm
except ImportError:
    litellm = None

def verify_provider(model: str, test_prompt: str = "Test") -> dict:
    start_time = time.time()
    
    # Pre-check env vars based on standard litellm requirements
    if "gpt" in model.lower() and not os.environ.get("OPENAI_API_KEY"):
        return {
            "status": "FAIL",
            "latency": 0.0,
            "error": "Missing OPENAI_API_KEY environment variable."
        }
    if "claude" in model.lower() and not os.environ.get("ANTHROPIC_API_KEY"):
        return {
            "status": "FAIL",
            "latency": 0.0,
            "error": "Missing ANTHROPIC_API_KEY environment variable."
        }
        
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=5,
            timeout=10
        )
        latency = time.time() - start_time
        return {
            "status": "PASS",
            "latency": latency,
            "error": None
        }
    except Exception as e:
        latency = time.time() - start_time
        return {
            "status": "FAIL",
            "latency": latency,
            "error": str(e)
        }

def main():
    print("--- Verifying Live Connectivity ---")
    
    if not litellm:
        print("Error: litellm is not installed.")
        return
        
    providers_to_test = [
        {"provider": "OpenAI", "model": "gpt-4-turbo"},
        {"provider": "Anthropic", "model": "claude-3-sonnet-20240229"}
    ]
    
    report_lines = [
        "# Provider Connectivity Report",
        f"**Generated:** {datetime.utcnow().isoformat()}",
        "",
        "| Provider | Model | Status | Latency (s) | Error Details |",
        "|----------|-------|--------|-------------|---------------|"
    ]
    
    all_passed = True
    
    for pt in providers_to_test:
        print(f"Pinging {pt['model']}...")
        result = verify_provider(pt["model"])
        
        status_icon = "✅ PASS" if result["status"] == "PASS" else "❌ FAIL"
        if result["status"] == "FAIL":
            all_passed = False
            
        error_msg = result["error"] if result["error"] else "-"
        # Escape pipes for markdown table
        error_msg = error_msg.replace("|", "-").replace("\n", " ")
        
        report_lines.append(f"| {pt['provider']} | {pt['model']} | {status_icon} | {result['latency']:.4f} | {error_msg} |")
        
    report_lines.append("")
    report_lines.append(f"**Overall Status:** {'READY' if all_passed else 'FAILED'}")
    
    if not all_passed:
        report_lines.append("\n> [!CAUTION]")
        report_lines.append("> **EXECUTION BLOCKED.** Valid API credentials are required to proceed with M11.6.3.")
        report_lines.append("> The system cannot simulate or fabricate evidence.")
        
    base_dir = Path(__file__).parent.parent
    report_path = base_dir / "docs" / "evaluation" / "PROVIDER_CONNECTIVITY_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Connectivity report written to: {report_path}")
    
    # Return exit code based on success
    import sys
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
