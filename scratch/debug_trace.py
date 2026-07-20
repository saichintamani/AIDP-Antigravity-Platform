import os, sys, json
sys.path.insert(0, os.path.abspath('src'))
from aidp.discovery.workflow import AutonomousDiscoveryOrchestrator

class MockGateway:
    def query(self, prompt, schema_hint=None, **kwargs):
        if "consensus" in prompt.lower() or "review" in prompt.lower() or "debate" in prompt.lower():
            return {"consensusReached": True, "consensusReport": "Mock", "critiques": [{"decision": "approve"}]}
        if schema_hint:
            if isinstance(schema_hint, type):
                try:
                    return schema_hint()
                except Exception:
                    return {}
            return schema_hint
        return {'mock': 'data'}

o = AutonomousDiscoveryOrchestrator(gateway=MockGateway(), requires_human_approval=False)
try:
    s = o.run_discovery_cycle('Can we use a synthetic peptide to inhibit the aggregation of alpha-synuclein in Parkinsons disease')
    for t in s.trace:
        evt = t.get('event', '')
        meta = json.dumps(t.get('metadata', {}), default=str)[:200]
        print(f"{evt}: {meta}")
    print(f"\nFinal state: {s.state}")
    print(f"Contradictions: {len(s.contradictions)}")
    print(f"Hypothesis: {s.hypothesis}")
except Exception as e:
    import traceback
    traceback.print_exc()
