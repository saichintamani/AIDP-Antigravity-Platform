import json
import re
with open('docs/evaluation/evidence/LIVE_RAW_OUTPUTS.json') as f:
    data = json.load(f)

finished = 0
failed = 0
for item in data:
    match = re.search(r'\*\*Final State:\*\*\s*(.+)', str(item.get('aidp_output')))
    state = match.group(1).strip() if match else 'UNKNOWN'
    if state == 'FINISHED':
        finished += 1
    elif state == 'FAILED':
        failed += 1
    print(f"{item.get('case_id')}: {state}")

print(f"Total Approved (FINISHED): {finished}")
print(f"Total Failed: {failed}")
