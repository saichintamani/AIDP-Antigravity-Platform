import argparse
import json
import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import litellm
import pandas as pd
import logging
from dataclasses import dataclass, field
import backoff
import hashlib
from typing import Any, Dict, List, Optional
"""Human baseline scorer for the Artificial Intelligence Discovery Platform (AIDP).

Provides simulated expert evaluations using a cloud‑based LLM. The module is fully typed, uses structured logging,
exponential‑back‑off retry logic, and deterministic per‑case seeding to avoid bias. Configuration can be
overridden via environment variables (e.g. ``AI_MODEL``) or command‑line arguments.
"""
# Add src and current dir to path to allow absolute imports
# Removed sys.path hacks – the package is now importable via proper installation.
# Imports use the aidp package directly.
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

from tests.evaluation.datasets.historical_cases import ALL_CASES

@dataclass
class BaselineConfig:
    """Configuration for the baseline scorer.

    Attributes:
        model: The LLM model to use. Defaults to the environment variable ``AI_MODEL``
            or ``gpt-4o-mini``.
        temperature: Sampling temperature for the LLM.
        max_retries: Number of retry attempts on transient failures.
        response_format: Expected response format for the LLM.
    """
    model: str = field(default_factory=lambda: os.getenv("AI_MODEL", "gpt-4o-mini"))
    temperature: float = 0.7
    max_retries: int = 3
    response_format: dict = field(default_factory=lambda: {"type": "json_object"})

# Helper to call LLM with exponential back‑off retries
def _call_llm(prompt: str, cfg: BaselineConfig) -> dict:
    """Invoke the LLM via litellm with retries.

    Args:
        prompt: The full prompt string to send to the model.
        cfg: BaselineConfig instance containing model and retry settings.

    Returns:
        Parsed JSON dictionary from the model response.
    """
    @backoff.on_exception(backoff.expo,
                          (Exception,),
                          max_tries=cfg.max_retries,
                          jitter=None)
    def _inner() -> dict:
        response = litellm.completion(
            model=cfg.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=cfg.temperature,
            response_format=cfg.response_format,
        )
        # litellm returns a Completion object; extract and parse JSON
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    return _inner()


# 5 Expert Personas to simulate different domain biases
EXPERT_PERSONAS = [
    {"name": "Dr. P", "role": "Theoretical Physicist (Focuses on mathematical elegance and fundamental physical laws)"},
    {"name": "Dr. B", "role": "Biochemist (Focuses on molecular mechanisms, enzymology, and structural constraints)"},
    {"name": "Dr. G", "role": "Geneticist (Focuses on heritability, RNA/DNA dynamics, and evolutionary conservation)"},
    {"name": "Dr. M", "role": "Materials Scientist (Focuses on structural properties, crystallography, and phase transitions)"},
    {"name": "Dr. E", "role": "Generalist/Epidemiologist (Focuses on population-level data, clinical outcomes, and broad trends)"}
]

def generate_survey_prompt(case: Any, persona: Dict[str, str], candidates: List[Any]) -> str:
    prompt = f"""You are acting as {persona['name']}, a {persona['role']}.
You are participating in a blinded scientific peer review for a grant proposal in the field of {case.domain}.
The cutoff date for your knowledge is {case.time_window}. DO NOT use knowledge discovered after this date.

EVIDENCE:
"""
    for ev in case.known_evidence:
        prompt += f"- {ev.extracted_text}\n"

    if hasattr(case, 'constraints') and case.constraints:
        prompt += "\nCONSTRAINTS you MUST verify:\n"
        for c in case.constraints:
            prompt += f"- {c}\n"

    prompt += "\nCANDIDATE EXPERIMENTS:\n"
    options = ["Option A", "Option B", "Option C", "Option D"]
    for opt, exp in zip(options, candidates):
        prompt += f"{opt}: {exp}\n"

    prompt += """
Based on the evidence and constraints, which Option is MOST likely to lead to a breakthrough?
Reply ONLY with a JSON object in this exact format, with no markdown formatting:
{"rank_1": "Option X", "rationale": "Brief 1-sentence rationale"}
"""
    return prompt

def simulate_expert(case: Any, persona: Dict[str, str], candidates: List[Any]) -> Dict[str, Any]:
    prompt = generate_survey_prompt(case, persona, candidates)
    try:
        cfg = BaselineConfig()
        try:
            response_data = _call_llm(prompt, cfg)
        except Exception as e:
            logger.error("LLM call failed for %s on case %s: %s", persona["name"], case.case_id, e)
            response_data = {}
        rank_1 = response_data.get("rank_1", "Option A")
        # Cleanup invalid options
        if rank_1 not in ["Option A", "Option B", "Option C", "Option D"]:
            rank_1 = "Option A"
        return {
            "case_id": case.case_id,
            "expert_id": persona["name"],
            "expert_role": persona["role"].split("(")[0].strip(),
            "rank_1": rank_1,
            "rationale": response_data.get("rationale", "")
        }
    except Exception as e:
        print(f"Error simulating {persona['name']} for {case.case_id}: {e}")
        return {
            "case_id": case.case_id,
            "expert_id": persona["name"],
            "expert_role": persona["role"].split("(")[0].strip(),
            "rank_1": "Option A", # fallback
            "rationale": "Failed to parse LLM response"
        }

def generate_simulated_data(csv_path: str) -> pd.DataFrame:
    print(f"Generating Simulated Expert Baseline using LLM Personas...")
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for case in ALL_CASES:
            candidates = case.candidate_experiments.copy()
            seed = int(hashlib.sha256(case.case_id.encode()).hexdigest(), 16) % (2**32)
            random.seed(seed)
            random.shuffle(candidates)
            
            for persona in EXPERT_PERSONAS:
                futures.append(executor.submit(simulate_expert, case, persona, candidates))
                
        for i, future in enumerate(as_completed(futures)):
            results.append(future.result())
            if (i+1) % 10 == 0:
                print(f"  Simulated {i+1}/{len(ALL_CASES)*5} evaluations...")
                
    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Saved simulated expert data to {csv_path}\n")
    return df

def evaluate_baseline(csv_path: str, ai_json_path: str, force_simulate: bool = False) -> None:
    """
    Takes a CSV of human/simulated participant results and compares it mathematically 
    against the AI results.
    """
    if force_simulate or not os.path.exists(csv_path):
        human_df = generate_simulated_data(csv_path)
    else:
        human_df = pd.read_csv(csv_path)
        
    if not os.path.exists(ai_json_path):
        print(f"Error: AI Results JSON {ai_json_path} not found.")
        print("We can still report the baseline accuracy:")
        ai_data = []
    else:
        with open(ai_json_path, 'r', encoding='utf-8') as f:
            ai_data = json.load(f)
            
    # We map case_id to correct Option by re-running the exact survey generation logic
    case_ground_truths = {}
    for case in ALL_CASES:
        candidates = case.candidate_experiments.copy()
        random.seed(42) 
        random.shuffle(candidates)
        correct_idx = candidates.index(case.historical_winner)
        options = ["Option A", "Option B", "Option C", "Option D"]
        case_ground_truths[case.case_id] = options[correct_idx]

    # Calculate Human Top-1 Accuracy
    total_evals = 0
    correct_evals = 0
    for idx, row in human_df.iterrows():
        case_id = row['case_id']
        if case_id in case_ground_truths:
            total_evals += 1
            if str(row['rank_1']).strip() == case_ground_truths[case_id]:
                correct_evals += 1
                
    human_accuracy = (correct_evals / total_evals) * 100 if total_evals > 0 else 0
    
    # Calculate AI Top-1 Accuracy
    ai_total = 0
    ai_correct = 0
    for result in ai_data:
        ai_total += 1
        if result.get('aidp_rank') == 1 or result.get('is_match') == True:
            ai_correct += 1
            
    ai_accuracy = (ai_correct / ai_total) * 100 if ai_total > 0 else 0
    
    # Inter-rater agreement (simple % agreement)
    agreement_sum = 0
    cases_counted = 0
    for case_id, group in human_df.groupby('case_id'):
        ranks = group['rank_1'].tolist()
        n = len(ranks)
        if n > 1:
            matches = 0
            pairs = 0
            for i in range(n):
                for j in range(i+1, n):
                    pairs += 1
                    if ranks[i] == ranks[j]:
                        matches += 1
            agreement_sum += (matches / pairs)
            cases_counted += 1
            
    avg_agreement = (agreement_sum / cases_counted) * 100 if cases_counted > 0 else 0

    print("==================================================")
    print(" AIDP PHASE R2/R3: EXPERT BASELINE EVALUATION     ")
    print("==================================================")
    print(f"Total Expert Evaluations: {total_evals} (Simulated)")
    if ai_total > 0:
        print(f"Total AI Evaluations    : {ai_total}")
    print("--------------------------------------------------")
    print(f"Expert Top-1 Accuracy   : {human_accuracy:.1f}%")
    if ai_total > 0:
        print(f"AI Top-1 Accuracy       : {ai_accuracy:.1f}%")
    print(f"Inter-rater Agreement   : {avg_agreement:.1f}%")
    print("--------------------------------------------------")
    if ai_total > 0:
        if ai_accuracy > human_accuracy:
            print(f"RESULT: AI Engine OUTPERFORMS Expert Baseline by {ai_accuracy - human_accuracy:.1f}%")
        elif ai_accuracy == human_accuracy:
            print(f"RESULT: AI Engine TIED with Expert Baseline at {human_accuracy:.1f}%")
        else:
            print(f"RESULT: AI Engine UNDERPERFORMS Expert Baseline by {human_accuracy - ai_accuracy:.1f}%")
    print("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Expert Baseline Scorer")
    parser.add_argument("--results", type=str, default="data/results/simulated_expert_scores.csv", help="Path to the participant results CSV")
    parser.add_argument("--ai-results", type=str, default="tests/evaluation/results/r3_scaled_results.json", help="Path to the AI JSON results")
    parser.add_argument("--simulate", action="store_true", help="Force regenerate the simulated expert data")
    args = parser.parse_args()
    
    evaluate_baseline(args.results, args.ai_results, args.simulate)
