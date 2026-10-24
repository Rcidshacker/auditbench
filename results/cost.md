# Cost per Article judgement (20 items, five-section files, Token Factory list prices)

| method | calls | input tokens | output tokens | USD per Article | USD per 5-Article file | wall time per Article |
|---|---|---|---|---|---|---|
| One whole-file Nemotron 3 Ultra call | 1.00 | 6,580 | 338 | $0.00759 | $0.0380 | 2.9 s |
| AuditBench Screener | 3.40 | 6,146 | 1,045 | $0.00172 | $0.0086 | 6.5 s |

Escalated to Ultra on 40% of this sample (v2 evaluation: 38%). Whole-file Ultra costs 4.4x the Screener per Article. Prices (USD per 1M tokens, in/out): Nano 0.06/0.24, Ultra 1.00/3.00. A 5-Article file needs 5 judgements either way. Wall time is one sequential measurement from India and includes network latency.
