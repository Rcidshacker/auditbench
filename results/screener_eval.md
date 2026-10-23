# Screener vs whole-file judge on Nebius Token Factory

120/120 AIReg-Bench items; each target excerpt placed first in a 5-section technical file.

| method | QWK vs experts | MAE | false clearance (expert non-compliant judged ≥4) | needs-review rate |
|---|---|---|---|---|
| Whole-file Nemotron 3 Nano (AIReg-Bench prompt) | 0.347 | 1.125 | 37.0% (27/73) | n/a |
| AuditBench Screener (per-section, 3× Nano + Ultra escalation) | 0.769 | 0.613 | 5.5% (4/73) | 20.0% |

Escalated to Nemotron 3 Ultra on 38% of items.