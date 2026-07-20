# AIDP Reproducibility Audit

**Date:** 2026-07-14T22:07:15.504520
**Status:** ✅ PASSED
**Execution Time:** 3.86 seconds

## Determinism Constraints
- `PYTHONHASHSEED`: 42
- `AIDP_DETERMINISTIC_MODE`: 1

## Execution Log
```text
============================= test session starts =============================
platform win32 -- Python 3.13.12, pytest-8.3.4, pluggy-1.5.0 -- C:\Users\saich\anaconda3\python.exe
cachedir: .pytest_cache
rootdir: D:\My projects\AIDP (Artificial Intelligence Discovery Platform)
configfile: pytest.ini
plugins: anyio-4.7.0, asyncio-0.24.0, cov-7.1.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collecting ... collected 9 items / 5 deselected / 4 selected

tests/evaluation/track_b/test_crispr_replay.py::test_crispr_historical_replay PASSED [ 25%]
tests/evaluation/track_c/test_red_team_containment.py::test_red_team_citation_ring_containment PASSED [ 50%]
tests/federation/test_federation_benchmarks.py::test_benchmark_1_truth_propagation PASSED [ 75%]
tests/intelligence/test_symbolic_solver.py::test_constraint_intelligence_unsat_temporal PASSED [100%]

======================= 4 passed, 5 deselected in 1.91s =======================

```
