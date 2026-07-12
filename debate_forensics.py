import json

debate_cases = [
    "case-oncology-004",
    "case-genetics-002",
    "case-genetics-003",
    "case-neuroscience-003",
    "case-immunology-003",
    "case-materials-002"
]

with open('docs/evaluation/evidence/LIVE_RAW_OUTPUTS.json') as f:
    outputs = json.load(f)

for item in outputs:
    if item['case_id'] in debate_cases:
        print(f"\n{'='*60}")
        print(f"CASE: {item['case_id']}")
        print(f"{'='*60}")
        print(f"Hypothesis: {json.dumps(item.get('hypothesis', {}), indent=2)}")
        print(f"Experimental Design: {json.dumps(item.get('experiment_design', {}), indent=2)}")
        print(f"Debate Record: {json.dumps(item.get('debate_record', {}), indent=2)}")
