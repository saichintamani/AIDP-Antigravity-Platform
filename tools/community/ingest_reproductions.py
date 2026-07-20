#!/usr/bin/env python3
import json
import re
import os

def ingest_reproductions(log_path, output_path):
    print("==================================================")
    print(" ANTIGRAVITY REPRODUCTION INGESTION")
    print("==================================================\n")
    
    if not os.path.exists(log_path):
        print(f"[ERROR] Reproduction log not found: {log_path}")
        return

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find each reviewer block
    # Matches: ### [Reviewer Name] followed by bullet points
    block_pattern = re.compile(r'### \[(.*?)\]\n(.*?)(?=\n### |$)', re.DOTALL)
    
    reproductions = []
    
    for match in block_pattern.finditer(content):
        reviewer = match.group(1).strip()
        body = match.group(2)
        
        entry = {"reviewer": reviewer}
        
        # Extract fields
        date_match = re.search(r'- \*\*Date\*\*: (.*)', body)
        release_match = re.search(r'- \*\*Target Release\*\*: (.*)', body)
        hardware_match = re.search(r'- \*\*Hardware\*\*: (.*)', body)
        model_match = re.search(r'- \*\*Model Version\*\*: (.*)', body)
        outcome_match = re.search(r'- \*\*Outcome\*\*: \[(.*?)\]', body)
        leakage_match = re.search(r'- \*\*Leakage Rate Observed\*\*: (.*?)%', body)
        
        if date_match: entry['date'] = date_match.group(1).strip()
        if release_match: entry['release'] = release_match.group(1).strip()
        if hardware_match: entry['hardware'] = hardware_match.group(1).strip()
        if model_match: entry['model'] = model_match.group(1).strip()
        if outcome_match: entry['outcome'] = outcome_match.group(1).strip()
        
        if leakage_match:
            try:
                entry['leakage_rate'] = float(leakage_match.group(1).strip())
            except ValueError:
                entry['leakage_rate'] = None
                
        # Skip the dummy template entry if someone left it as "YYYY-MM-DD" or similar
        if entry.get('date') == 'YYYY-MM-DD':
            continue
            
        reproductions.append(entry)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(reproductions, f, indent=4)
        
    print(f"Ingested {len(reproductions)} external reproductions.")
    print(f"Database saved to: {output_path}")

if __name__ == "__main__":
    log_file = "REPRODUCTION_LOG.md"
    out_file = "data/ANTIGRAVITY_EVIDENCE_V1/community_evidence.json"
    ingest_reproductions(log_file, out_file)
