import json
with open('docs/evaluation/evidence/LIVE_RUNTIME_METRICS.json') as f: metrics = json.load(f)
with open('docs/evaluation/evidence/LIVE_RAW_OUTPUTS.json') as f: outputs = json.load(f)
with open('docs/evaluation/evidence/LIVE_GOVERNANCE_AUDIT.json') as f: gov = json.load(f)
for i in range(len(metrics)):
    c_id = metrics[i]['case_id']
    b_s = metrics[i]['baseline_metrics']['scientific_correctness']
    a_s = metrics[i]['aidp_metrics']['scientific_correctness']
    if a_s < b_s:
        print(f'\n--- {c_id} ---')
        try:
            gov_passed = gov[i]['decisions'][0]['passed']
            print(f'Gov Result: {gov_passed}')
            if not gov_passed:
                print(f"Blocking Issues: {gov[i]['decisions'][0]['issues']}")
            else:
                print(f"AIDP Output Snippet: {outputs[i]['aidp_output'][:200]}...")
        except Exception as e:
            print(f"Error accessing governance data: {e}")
