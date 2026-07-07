# Release Blocker Register

## Critical Blockers
| ID | Blocker | Description | Resolution Path |
|---|---|---|---|
| BLK-001 | Missing API Credentials | The execution environment lacks `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`, causing immediate abortion of the physical benchmark suite. | Inject valid credentials into the shell environment via `export` or `.env`. |
| BLK-002 | Zero Empirical Evidence | Because BLK-001 aborts execution, no actual data exists to prove AIDP's scientific capability. Releasing the system now would constitute a breach of scientific integrity. | Resolve BLK-001 and execute `scripts/run_live_discoverybench.py`. |

## Major Blockers
*None currently identified. The framework is architecturally and operationally complete.*

## Minor Blockers
*None currently identified.*
