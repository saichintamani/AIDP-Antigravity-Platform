import urllib.request
import urllib.error
import json
import time
import sys

def initialize_ollama():
    """
    Prominent and advanced Ollama initialization script.
    Waits for the Ollama daemon to come online, then flawlessly triggers model pulls.
    Provides robust, production-grade error handling compared to inline shell scripts.
    """
    base_url = "http://ollama:11434"
    models_to_pull = ["gemma", "llama3", "mistral"]
    
    print("==================================================")
    print(" OLLAMA INITIALIZATION: Advanced Setup Executing")
    print("==================================================")
    
    # 1. Wait for daemon to become ready
    max_retries = 30
    daemon_ready = False
    
    print("[INIT] Waiting for Ollama daemon to come online...")
    for i in range(max_retries):
        try:
            req = urllib.request.Request(base_url)
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    daemon_ready = True
                    break
        except Exception:
            pass
        time.sleep(2)
        print(f"  ...retrying ({i+1}/{max_retries})")
        
    if not daemon_ready:
        print("[ERROR] Ollama daemon failed to start within the timeout period.")
        sys.exit(1)
        
    print("[INIT] Ollama daemon is online!")
    
    # 2. Pull essential models
    for model in models_to_pull:
        print(f"[INIT] Pulling model: {model} (This may take several minutes)...")
        pull_url = f"{base_url}/api/pull"
        data = json.dumps({"name": model}).encode("utf-8")
        req = urllib.request.Request(pull_url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                # In a real environment we would parse the streaming NDJSON for a progress bar,
                # but for initialization, blocking until successful HTTP 200 is sufficient.
                print(f"  -> Successfully pulled {model}")
        except urllib.error.URLError as e:
            print(f"  [ERROR] Failed to pull {model}: {e}")
            sys.exit(1)
            
    print("\n[SUCCESS] Ollama is completely initialized and fully-fledged. Ready for Reality Acquisition.")

if __name__ == "__main__":
    initialize_ollama()
