#!/usr/bin/env python3
"""
AlignEval: Zero-dependency blinded evaluation survey generator.
Generates cryptographically seeded, randomized Markdown surveys from structured JSON.
"""

import json
import random
import sys
import os
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Generate blinded evaluation surveys from JSON.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument("--output_dir", "-o", default="out", help="Directory to save the generated markdown.")
    return parser.parse_args()

def generate_markdown(data):
    case_id = data.get("case_id", "UNKNOWN_CASE")
    domain = data.get("domain", "General")
    time_window = data.get("time_window", "None specified")
    difficulty = data.get("difficulty_rating", "Standard")
    
    # Deterministic shuffle to prevent position bias but ensure reproducibility
    candidates = data.get("candidate_experiments", [])
    random.seed(case_id)
    random.shuffle(candidates)
    
    markdown = f"# Expert Evaluation Survey: {domain}\n\n"
    markdown += f"**Case ID:** {case_id}\n"
    markdown += f"**Historical Time Window:** {time_window}\n"
    markdown += f"**Difficulty Rating:** {difficulty}\n\n"
    
    markdown += "## Instructions\n"
    markdown += "You are acting as a peer-reviewer evaluating grant proposals or experimental directions at the cutoff date specified above. You MUST NOT use any knowledge discovered after this date. \n\n"
    markdown += f"Based **strictly on the evidence provided below**, please rank the candidate experiments from 1 (Most likely to succeed) to {len(candidates)} (Least likely).\n\n"
    markdown += "---\n\n"
    
    markdown += "## 1. Available Evidence\n\n"
    for ev in data.get("known_evidence", []):
        markdown += f"### {ev.get('source_id', 'EVIDENCE')} ({ev.get('source_type', 'Publication')})\n"
        markdown += f"> {ev.get('extracted_text', '')}\n\n"
        
        tags = ev.get('tags', [])
        if tags:
            markdown += f"- **Tags:** {', '.join(tags)}\n"
            
        constraints = ev.get('mathematical_constraints', [])
        if constraints:
            markdown += f"- **Constraints:** {', '.join(constraints)}\n"
        markdown += "\n"

    constraints = data.get("constraints", [])
    if constraints:
        markdown += "### Explicit Constraints\n"
        for c in constraints:
            markdown += f"- {c}\n"
        markdown += "\n"

    markdown += "---\n\n## 2. Candidate Experiments to Rank\n\n"
    
    for i, exp in enumerate(candidates):
        markdown += f"**Option {chr(65+i)}:**\n{exp}\n\n"
        
    markdown += "---\n\n## 3. Your Ranking & Rationale\n\n"
    markdown += "**Top Choice (Rank 1):** Option [ ]\n"
    for rank in range(2, len(candidates) + 1):
        markdown += f"**Rank {rank}:** Option [ ]\n"
    markdown += "\n"
    
    markdown += "**Rationale for Top Choice (Max 150 words):**\n\n\n\n"

    return markdown, case_id

def main():
    args = parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)
        
    markdown_content, case_id = generate_markdown(data)
    
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    output_filename = f"survey_{case_id.lower()}.md"
    output_path = out_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Success! Generated blinded survey: {output_path}")

if __name__ == "__main__":
    main()
