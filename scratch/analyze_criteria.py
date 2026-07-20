import json
with open('C:/Users/saich/.gemini/antigravity-ide/brain/d017cc73-ba47-455a-8b4f-ae4d9a0b014b/SPL_VALIDATION_EVIDENCE.json') as f:
    data = json.load(f)

for item in data:
    print(f"Case: {item['case_id']}")
    print(f"Success Criteria: {item['new_design'].get('successCriteria')}")
    print(f"Failure Criteria: {item['new_design'].get('failureCriteria')}")
    print("Critiques:")
    for c in item['new_critiques']:
        if c['decision'] == 'reject':
            print(f"  {c['role']}: {c.get('blockingIssues')}")
            print(f"    Evidence: {c.get('evidence')}")
    print()
