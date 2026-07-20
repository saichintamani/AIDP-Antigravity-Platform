#!/bin/bash
set -e

echo "==========================================================="
echo " Antigravity Reproducibility Script (Layer 1 & 2)          "
echo "==========================================================="
echo ""
echo "[1/4] Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed. Please install Python 3.10+."
    exit 1
fi

if ! command -v ollama &> /dev/null; then
    echo "ERROR: ollama is not installed. Please install Ollama from https://ollama.com to run local evaluations."
    exit 1
fi

echo "[2/4] Setting up isolated environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Pulling local model (llama3.1:8b) for deterministic evaluation..."
ollama pull llama3.1:8b

echo "[4/4] Executing AlignEval generation..."
# Run the AlignEval survey generation on the historical dataset
python tools/align-eval/align_eval.py

echo ""
echo "==========================================================="
echo " Reproduction Complete.                                    "
echo " The blinded surveys have been successfully regenerated    "
echo " and can be found in the /surveys directory.               "
echo "                                                           "
echo " To run the Simulated Human Evaluation, execute:           "
echo " python tools/reality-acquisition/simulate_evaluators.py   "
echo "==========================================================="
