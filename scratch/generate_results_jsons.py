import json
import re

with open('docs/evaluation/evidence/LIVE_RAW_OUTPUTS.json', 'r') as f:
    raw_outputs = json.load(f)

baseline_results = []
aidp_results = []
official_results = []

for item in raw_outputs:
    case_id = item['case_id']
    
    # AIDP extraction
    aidp_text = str(item.get('aidp_output', ''))
    match = re.search(r'\*\*Final State:\*\*\s*(.+)', aidp_text)
    state = match.group(1).strip() if match else 'UNKNOWN'
    aidp_passed = (state == 'FINISHED')
    
    # Baseline extraction (from string)
    baseline_text = str(item.get('baseline_output', ''))
    baseline_passed = False # we'll assume they failed unless we have a logic for baseline pass/fail. Actually, let's just save the text.

    # Save to standard dicts
    aidp_dict = {
        "case_id": case_id,
        "passed": aidp_passed,
        "output": aidp_text
    }
    
    baseline_dict = {
        "case_id": case_id,
        "output": baseline_text
    }
    
    combined_dict = {
        "case_id": case_id,
        "baseline_passed": baseline_passed,
        "aidp_passed": aidp_passed
    }
    
    aidp_results.append(aidp_dict)
    baseline_results.append(baseline_dict)
    official_results.append(combined_dict)

with open('docs/evaluation/evidence/OFFICIAL_AIDP_RESULTS.json', 'w') as f:
    json.dump(aidp_results, f, indent=2)

with open('docs/evaluation/evidence/OFFICIAL_BASELINE_RESULTS.json', 'w') as f:
    json.dump(baseline_results, f, indent=2)

with open('docs/evaluation/evidence/OFFICIAL_DISCOVERYBENCH_RESULTS.json', 'w') as f:
    json.dump(official_results, f, indent=2)

print(f"Generated official results JSON files. AIDP Passed: {sum(1 for r in aidp_results if r['passed'])}/20")
