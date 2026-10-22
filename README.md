# AuditBench: are LLM compliance auditors reliable, and can they be talked into a "compliant"?

A small, reproducible study built for the Pivotal Research Q1 2027 application, aimed at Merlin Stein and Kevin Wei's "Automating AI governance" stream. Alexandra Abbas's scanner-reliability project is the secondary target.

**Question.** As the EU AI Act's high-risk obligations approach (Annex III from 2 Dec 2027), providers and notified bodies will use LLMs to pre-screen technical documentation against Articles 9–15. AIReg-Bench showed frontier LLMs can agree with legal experts. It did not test two things a regulator needs before relying on such a tool:

1. **Reliability.** Does the same auditor give the same verdict twice?
2. **Robustness.** Does the verdict move when the documentation gains text that adds *no evidence*? Tested with an unsupported "we are certified compliant" statement, a "pre-approved by the AI Office" note to the reviewer, a vague negative remark, and pure reformatting.

**What's here**

| Path | Contents |
|---|---|
| `auditbench/` | Harness: data loader (undoes AIReg-Bench's label permutation), auditor configs, perturbations, OpenJev client, metrics, analysis |
| `results/runs*.jsonl` | Every auditor call: config, perturbation, item, sample, score |
| `results/RESULTS.md` | Generated tables |
| `REPORT.md` | Findings, limitations, risk register, policy recommendations |
| `notes/` | Fellowship facts, mentor map, EU AI Act / NIST AI RMF primer, related work |
| `external/aireg-bench/` | Upstream benchmark, cloned locally by the setup step below (no licence upstream, so it isn't redistributed here) |

**Auditors tested**

| Config | What it is |
|---|---|
| `generative` | `diffusiongemma-26b` text generation with AIReg-Bench's *exact* original prompt, so it's comparable to the published frontier numbers |
| `holistic` | OpenJev System One `score` question (calibrated distribution over 1–5) with outline + Article + documentation |
| `holistic_noarticle` / `holistic_nooutline` | Context ablations (the "Audit tools of the trade" question applied to compliance) |
| `decomposed` | One yes/no question per numbered Article paragraph; score = 1 + 4·min P(yes) (mean also logged) |

**Run it**

```bash
uv venv .venv && uv pip install --python .venv openpyxl pandas numpy scipy scikit-learn krippendorff
git clone --depth 1 https://github.com/camlsys/aireg-bench external/aireg-bench
.venv/Scripts/python -m auditbench.metrics            # self-check
.venv/Scripts/python -m auditbench.run --configs holistic --perturbations none assurance --k 3
.venv/Scripts/python -m auditbench.analyze            # writes results/RESULTS.md
```

Needs `OPENJEV_API_KEY` in the environment (Codiv free tier). Runs are cached and resumable. A full grid is ~5,800 calls and ~15M tokens.
