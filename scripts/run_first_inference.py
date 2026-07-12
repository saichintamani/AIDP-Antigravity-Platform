import json
import time
import os
import traceback
from pathlib import Path

try:
    import litellm
except ImportError:
    litellm = None

def main():
    if not litellm:
        print("litellm is required.")
        return

    model = "ollama/qwen2.5:0.5b" # using the small model to test quickly
    prompt = "Respond with the single word: READY"
    
    # We may need to pass api_base if litellm doesn't default to the right one, 
    # but litellm defaults ollama to http://localhost:11434 automatically.
    
    print(f"Executing First Live Inference Verification (Local Provider)...")
    print(f"Model: {model}")
    print(f"Prompt: {prompt}")

    start_time = time.time()
    response = None
    cost = 0.0
    input_tokens = 0
    output_tokens = 0
    status = "SUCCESS"
    error_details = None

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        cost = 0.0 # Local inference is always $0.00
        input_tokens = response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0
        output_tokens = response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0
        response_text = response.choices[0].message.content
    except Exception as e:
        status = "FAILED"
        response_text = "N/A"
        error_details = str(e)
        print(f"Execution Failed: {error_details}")

    runtime = time.time() - start_time

    report = {
        "Provider": "Ollama (Localhost)",
        "Model": model,
        "Status": status,
        "Response": response_text,
        "PromptTokens": input_tokens,
        "CompletionTokens": output_tokens,
        "Cost": cost,
        "Latency": runtime,
        "ErrorDetails": error_details
    }

    base_dir = Path(__file__).parent.parent
    evidence_dir = base_dir / "docs" / "evaluation"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    with open(evidence_dir / "FIRST_LOCAL_INFERENCE_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Execution complete. Report written.")

if __name__ == "__main__":
    main()
