<div align="center">

# AuditBench Screener

**Catch what long technical files hide.**
EU AI Act pre-screening for Articles 9 to 15, section by section, with NVIDIA Nemotron on Nebius Token Factory.

[![Live demo](https://img.shields.io/badge/live%20demo-auditbench--screener.vercel.app-f0693d?style=flat-square)](https://auditbench-screener.vercel.app)
[![NVIDIA Nemotron](https://img.shields.io/badge/NVIDIA-Nemotron%203%20Nano%20%2B%20Ultra-76B900?style=flat-square&logo=nvidia&logoColor=white)](https://huggingface.co/nvidia)
[![Nebius Token Factory](https://img.shields.io/badge/Nebius-Token%20Factory-1f2937?style=flat-square)](https://nebius.com)
[![Python](https://img.shields.io/badge/python-FastAPI-3776AB?style=flat-square&logo=python&logoColor=white)](#run-it)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)

[**Try it**](https://auditbench-screener.vercel.app) · [**Watch the demo**](https://youtu.be/lllaV5v8RtQ) · [**Read the study**](REPORT.md)

<br>

<img src="docs/media/demo.gif" alt="AuditBench Screener screening a five-section technical file: the hidden Article 14 human-oversight violation is rated likely non-compliant, with quotes checked against the source." width="880">

<sub>Real run on the live site: a hidden Article 14 violation in a five-section technical file is caught. <a href="https://youtu.be/lllaV5v8RtQ">Full demo video (2:30, narrated)</a></sub>

</div>

---

## Why

From **2 December 2027**, high-risk AI systems in the EU must document compliance with Articles 9 to 15 of the AI Act. There is far too much documentation to read by hand, so reviewers and providers will reach for LLMs to pre-screen it.

Before building one, we tested whether LLM auditors can be trusted, on **120 documents labelled by legal experts** ([AIReg-Bench](https://huggingface.co/datasets/camlsys/AIReg-Bench)). The surprise wasn't fake approvals or rewrite attacks. It was **length**: put the violating section first in a full technical file, and the compliant sections after it hide it.

## The result

Same 120 expert-labelled files, violating section placed first in a five-section technical file, all run on Nebius Token Factory:

| | Agreement with experts (QWK) | Violations falsely cleared |
|---|:---:|:---:|
| Whole-file Nemotron 3 Nano | 0.347 | **37%** (27 of 73) |
| **AuditBench Screener** | **0.769** | **5.5%** (4 of 73) |

<sub>v1, single run: raw rows in <a href="results/screener_eval.jsonl"><code>results/screener_eval.jsonl</code></a> · table in <a href="results/screener_eval.md"><code>results/screener_eval.md</code></a></sub>

### Re-tested under a frozen protocol (v2)

We then pre-registered a stricter test in [`PLAN.md`](PLAN.md): stronger baselines, a held-out split by system, 3 repeat runs, bootstrap CIs, and files with headings removed. Missed violations over all 120 files, 95% CI:

| | Violations falsely cleared | Compliant files falsely rejected |
|---|:---:|:---:|
| Whole-file Nemotron 3 Nano (1 call / median of 3) | 52% / 47% | 2% / 0% |
| Whole-file Nemotron 3 Ultra (1 call) | **6.8%** [1, 14] | **6.4%** |
| AuditBench Screener | **4.1%** [0, 10] | 14.9% |
| Screener on files with no headings (whole text) | 0.0% to 4.1% | 8.5% to 10.6% |

What this changed:
- The Screener beats whole-file Nano by a wide margin. Against one whole-file Ultra call it is a statistical tie on missed violations, and it raises more false alarms.
- The gain comes from the **judging prompt** (one Article, ignore claims, count disclosed gaps), not from splitting the file. On files with no headings it does just as well.
- Run-to-run noise is real: three runs of the same whole-file judge gave 52%, 45% and 43%.

Full write-up: [`REPORT.md` §1c](REPORT.md) · tables: [`results/screener_eval_v2.md`](results/screener_eval_v2.md) · known-answer suite (14/14 pass): [`results/regression.md`](results/regression.md) · reproduce: `python -m screener.evaluate --split test --stage all`

## How it works

Every step answers a failure we measured.

```mermaid
flowchart LR
    A[Technical file] --> B[Split by<br/>Article heading]
    B --> C[Each section<br/>Art. 9, 10, 12, 14, 15<br/>judged on its own]
    C --> D[Nemotron 3 Nano<br/>3 parallel samples]
    D -->|agree| F[Verdict + verified quotes]
    D -->|disagree or on the fence| E[Nemotron 3 Ultra]
    E -->|agrees with Nano| F
    E -->|still disagrees| G[Human review]
    A -.-> H[Flag notes to the reviewer<br/>and unsupported claims]
    H -.->|ignored as evidence| F
```

| Step | The failure it fixes |
|---|---|
| **Judge one Article at a time** | Whole-file judges with a generic prompt let compliant sections mask a violation. The v2 re-test shows a targeted prompt is what closes this; splitting by heading adds little. Files without headings are judged as whole text (an Ultra segmenter exists, opt-in, and did not help). |
| **Sample three times** | A single LLM sample can flip its verdict between identical runs. |
| **Escalate to Ultra, then to a human** | Even three legal experts only partly agree (Krippendorff's α 0.657). Close calls go to a person instead of a guess. |
| **Flag claims, check quotes** | Reviewer-addressed notes are flagged and ignored. Evidence quotes appear only if they occur (near-)verbatim in the document. |

Engine: [`screener/engine.py`](screener/engine.py) · API + UI: [`screener/app.py`](screener/app.py), [`screener/static/index.html`](screener/static/index.html)

## Screenshots

| Landing | Hidden violation caught | Fake approval flagged |
|---|---|---|
| <img src="docs/media/landing.png" alt="Landing page"> | <img src="docs/media/result.png" alt="Article 14 likely non-compliant"> | <img src="docs/media/injected.png" alt="Pre-approval note flagged, still non-compliant"> |

## What the research found

The Screener sits on top of **AuditBench**, a study of LLM compliance auditors: 5,760 scored calls on OpenJev auditors, Nemotron runs on Token Factory, published frontier results, an adaptive Claude attacker with an independent verifier, and bootstrap confidence intervals. Full write-up in [`REPORT.md`](REPORT.md).

| Finding | Number |
|---|---|
| Best judges vs the published frontier (Gemini 2.5 Pro, GPT-5) | Statistically tied (QWK ≈ 0.85 to 0.88, paired bootstrap CIs) |
| Unsupported "certified compliant" / "pre-approved by the AI Office" text | **0** non-compliant documents cleared |
| Adaptive rewrite attack (Claude Sonnet attacker, independent verifier) | **1 of 32** succeeded |
| Simple holistic question vs per-paragraph checklist | Checklist is worse (QWK 0.64 vs 0.88) |
| Long multi-section files, violation first | **9.6% to 37%** false clearance, depending on the judge |
| Renaming every company and product | No effect (Δ +0.011, CI includes 0) |

## Run it

```bash
uv venv .venv && uv pip install --python .venv fastapi uvicorn
export NEBIUS_API_KEY=...                       # Windows: setx NEBIUS_API_KEY "..."
.venv/bin/python -m uvicorn screener.app:app --port 8000   # open http://localhost:8000
```

Reproduce the evaluation (needs the CC-BY benchmark locally):

```bash
git clone --depth 1 https://github.com/camlsys/aireg-bench external/aireg-bench
uv pip install --python .venv numpy pandas scipy scikit-learn krippendorff openpyxl
.venv/bin/python -m screener.evaluate          # Screener vs whole-file Nemotron, 120 files
.venv/bin/python -m auditbench.analyze         # the research tables in results/RESULTS.md
```

<details>
<summary><b>Repository map</b></summary>

| Path | What it is |
|---|---|
| `screener/` | The app: engine, FastAPI server, single-page UI, evaluation |
| `auditbench/` | Research harness: data loader, auditors, perturbations, providers (OpenJev, NVIDIA, Nebius, OpenRouter, Claude), metrics, adaptive attacker |
| `results/` | Every scored call (`runs*.jsonl`) and generated tables |
| `REPORT.md`, `PLAN.md` | Findings, limitations, risk register, policy notes; phase-2 plan |
| `notes/` | EU AI Act / NIST AI RMF primer, related work |
| `video/` | The demo video pipeline: CDP screen recording + edit in [Concat](https://github.com/jub0t/Concat) via its MCP server |
| `docs/media/` | Demo video, GIF and screenshots |

</details>

## Limits

- **A screening aid, not legal advice** or a conformity assessment. It tells a reviewer where to look.
- Evaluated on **synthetic, expert-labelled excerpts**. Real technical files are longer and messier.
- Covers **Articles 9, 10, 12, 14 and 15**, the core high-risk requirements.
- About **one Article in eight** goes to human review, on purpose.

## Built with

NVIDIA Nemotron 3 Nano and Nemotron 3 Ultra on **Nebius Token Factory** · Python · FastAPI · Vercel · demo edited in Concat.
Built for the **Nebius x NVIDIA Global AI Hackathon** (Best Apps and Agents track).

## Credits

Example documents and labels come from **AIReg-Bench** (Marino, Hunter, Jamali et al., 2025, [arXiv:2510.01474](https://arxiv.org/abs/2510.01474)), [CC-BY-4.0](https://huggingface.co/datasets/camlsys/AIReg-Bench). See [`NOTICE.md`](NOTICE.md). Code is [MIT](LICENSE).
