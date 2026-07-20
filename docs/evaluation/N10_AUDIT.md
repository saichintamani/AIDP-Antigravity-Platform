# N=10 Benchmark Audit Ledger

This ledger is the single source of truth for the project's evidence base. 
*A generated script is not evidence. A mock architecture run is not evidence.*
A case is only considered complete when both live LLM and live Human data have been collected and verified.

| Case | Dataset Complete | Survey Complete | LLM Tested | Human Tested |
| :--- | :--- | :--- | :--- | :--- |
| CRISPR | Yes | Yes | No (Mock Only) | Pending Pilot |
| Plate Tectonics | Yes | Yes | No (Mock Only) | Pending Pilot |
| Prions | Yes | Yes | No (Mock Only) | Pending Pilot |
| H. pylori | Yes | Yes | No (Mock Only) | No |
| Quasicrystals | Yes | Yes | No (Mock Only) | No |
| HT Superconductors | Yes | Yes | No (Mock Only) | No |
| RNAi | Yes | Yes | No (Mock Only) | No |
| mRNA LNP | Yes | Yes | No (Mock Only) | No |
| Helicase | Yes | Yes | No (Mock Only) | No |
| Gravitational Waves | Yes | Yes | No (Mock Only) | No |

### Definitions
- **Dataset Complete:** The historical evidence fragments (`EV_...`) and constraints are fully authored in the Python case file.
- **Survey Complete:** The blinded markdown survey has been generated without hindsight leakage.
- **LLM Tested:** The case has been run against a LIVE generative model (not a MockProvider) to produce empirical stability bounds.
- **Human Tested:** The case has been blindly evaluated by independent domain experts.
