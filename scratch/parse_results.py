import json

with open('scratch/spl_validation_results.json') as f:
    data = json.load(f)

for item in data:
    print(f"Case: {item['case_id']}")
    print(f"  Old Decision: rejected")
    print(f"  New Decision: {item['new_decision']}")
    has_controls = len(item['new_design'].get('controls', [])) > 0
    has_sample = 'sampleSize' in item['new_design']
    has_evidence = len(item['new_design'].get('evidence_to_claim_mapping', [])) > 0
    print(f"  Controls Generated: {has_controls}")
    print(f"  Sample Size Generated: {has_sample}")
    print(f"  Evidence Linked: {has_evidence}")
    for critique in item['new_critiques']:
        if critique['decision'] == 'reject':
            print(f"    {critique['role']} rejected: {critique['blockingIssues']}")
    print()
