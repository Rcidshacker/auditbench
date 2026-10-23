# AuditBench Screener

**Nebius x NVIDIA Global AI Hackathon, Best Apps and Agents track.** Paste an AI system's technical file, and NVIDIA Nemotron on **Nebius Token Factory** screens it against EU AI Act Articles 9, 10, 12, 14 and 15, section by section, without being fooled by fake approvals.

| On 120 expert-labelled files, violation section placed first | QWK vs experts | Violations falsely cleared |
|---|---|---|
| Whole-file Nemotron 3 Nano | 0.347 | 37% (27/73) |
| **AuditBench Screener** | **0.769** | **5.5% (4/73)** |

How it works (`screener/engine.py`):
1. Split the file into Article sections and judge each on its own. This is the fix for the long-file blind spot found below.
2. Run **Nemotron 3 Nano** 3× in parallel; escalate disagreement to **Nemotron 3 Ultra**; send unresolved cases to human review.
3. Flag reviewer-addressed notes and unsupported compliance claims, and ignore them as evidence.
4. Show only evidence quotes found (near-)verbatim in the document.

```bash
uv venv .venv && uv pip install --python .venv fastapi uvicorn
setx NEBIUS_API_KEY "..."      # Windows (or export NEBIUS_API_KEY=... on macOS/Linux)
.venv/Scripts/python -m uvicorn screener.app:app --port 8000   # open http://localhost:8000
python -m screener.evaluate    # reproduces the table above (needs the benchmark clone, see below)
```

The research behind it follows.

---

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
