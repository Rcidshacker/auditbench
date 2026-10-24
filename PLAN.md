# Phase 2 plan: closing the open limitations

Each workstream has its own module and its own `results/<ws>_*.jsonl`, so they run and fail independently. They share only `auditbench/data.py`, `metrics.py` and the provider layer. Constraints shared by all: OpenJev System One is capped at 60 req/min per key; NVIDIA NIM at ~40 req/min.

## Backends (verified 2026-10-22)

| Backend | Status | Cost | Limit | Used for |
|---|---|---|---|---|
| OpenJev System One + `diffusiongemma-26b` chat | working | free | 60 req/min; 100M + 10M tokens/mo | baseline auditors; L3; L5 |
| Claude via subscription (`claude -p`) | **blocked**: CLI OAuth expired, and `~/.claude/settings.json` routes the CLI to Atomic Chat (`127.0.0.1:1337`, nemotron). Fix: `claude setup-token` + bypass user settings | subscription | 5-hour usage windows | L1 (Haiku full, Sonnet subset) |
| NVIDIA NIM (build.nvidia.com) | **needs key** | free | ~40 req/min | L1 (3–4 open-weight models); L2 attacker + verifier |
| OpenRouter `:free` models | **needs key** | free | 50 req/day (1,000/day after a one-off $10 top-up) | L1 spot-check only, unless topped up |
| Groq | optional key | free | 1,000 req/day on gpt-oss-120b, 30/min | L1 (one model/day) |
| Google AI Studio (Gemini Flash) | optional key | free; **prompts may be used by Google**, fine for this public benchmark | per-model RPD | L1 (frontier-family comparison to the published Gemini numbers) |
| Atomic Chat local (`127.0.0.1:1337`) | app not running now | free | local GPU (RTX 4050, 6 GB) | L1 small local model; checks the "can a laptop audit?" angle |
| GitHub Models | unusable: endpoint returns a bare `OK` | – | – | dropped |
| Cerebras | card required since 2026 | – | – | dropped |

Keys: set them as **user environment variables in your own terminal** (`setx NAME "value"`), never in chat. The code reads `HKCU\Environment` directly, so no app restart is needed.

## L1: model coverage (more auditors, under the same perturbations)

- **Goal:** test whether "can't be talked into compliant" and "simple beats structured" hold beyond one model family.
- **Design:** a generic OpenAI-compatible provider plus a `claude -p` provider, reusing AIReg-Bench's verbatim prompt (`generative` config).
- **Per model:** 120 items × {none ×2 samples, assurance, authority, reformat} = 600 calls.
- **Models (target):**
  - Claude Haiku (full) + Claude Sonnet (none/assurance/authority only, 360 calls, to respect subscription limits)
  - NVIDIA: Llama-3.3-70B, DeepSeek-V3.x, Qwen3 (largest available), gpt-oss-120b
  - Gemini Flash (free tier) if a key is provided
  - one local model via Atomic Chat
- **Done when:** RESULTS.md has a per-model validity + perturbation table and REPORT §1 is rewritten with cross-model claims and their CIs.

## L2: adaptive red-team (the real robustness test)

- **Goal:** can an attacker *rewrite* a violating document so the auditor says compliant, while the violation is still described?
- **Design:**
  - **Targets:** 40 violation documents (8 per Article, mixed uses).
  - **Attacker loop:** up to 4 rounds. The attacker sees the document, the Article, the auditor's last score and (black-box) nothing else. Its instruction: keep every factual statement about how the system works, change framing, emphasis and structure, and add no false facts.
  - **Verifier:** a model from a different family from the attacker. It reads AIReg-Bench's own written violation statement (`violations/.../ScenarioN.txt`, `[c] Violation`) and judges whether the rewrite still describes that violation. It's also asked whether the rewrite adds claims not in the original.
  - **Success:** auditor score ≥ 4, violation preserved (P ≥ 0.8), and no new false facts.
  - **Transfer:** successful attacks are re-scored by the other auditors.
  - **Human check:** 10 attacked documents go into a review sheet for Ruchit to verify by hand. That number is reported separately; an automated verifier is not ground truth.
- **Done when:** attack success rate per auditor with a CI, transfer matrix, and the human-check agreement rate.

## L3: realistic length (dossier stress test)

- **Goal:** real Annex IV documentation is long and covers every Article at once. Does the auditor still find a violation buried in a dossier?
- **Design:**
  - **Dossier:** the target excerpt plus the four *compliant* excerpts for the other Articles of the same system and use (~5× longer, still label-preserving).
  - **Target position:** first, middle or last.
  - **Instruction:** judge only the target Article.
  - **Metrics:** validity vs experts, position effect, and "halo" (do compliant neighbour sections raise scores of violating targets?).
  - **Runs:** OpenJev holistic + generative first; L1 models later if budget allows.
- **Done when:** a table of validity by position, plus halo Δ with a CI.

## L4: ground-truth noise (analysis only, no API)

- Paired bootstrap CIs on QWK *differences*. Is OpenJev 0.877 vs Gemini 0.863 a real gap? (Probably not; say so.)
- Agreement with each individual expert, not just the median.
- Re-score on the high-agreement subset (all three experts within 1 point).
- AUROC against the *generation intent* labels (compliant vs violation file) as a second, independent ground truth.
- **Done when:** REPORT states which headline claims survive the CIs.

## L5: contamination probe (cheap)

- **Goal:** AIReg-Bench has been public since Oct 2025, so models may have memorised it.
- **Design:** a `rename` perturbation swaps company and system names for fresh ones (label-preserving). If scores are stable under renaming, memorised verdicts are less likely to drive results. Runs on OpenJev holistic + generative, then any L1 model.
- **Caveat:** this is a weak probe. It can show sensitivity to surface names, but stability doesn't prove the absence of memorisation.

## L6: synthetic → real documents (deferred, with a reason)

Expert-labelled real Annex IV documentation doesn't exist publicly, and we can't create expert labels. L3 is the realism step we can do now. A real-document pilot with notified-body reviewers is a fellowship-stage task: it's listed under next steps, not attempted.

## L7: Ruchit can defend it

`notes/06_interview_prep.md`: likely mentor questions with answers grounded in the numbers, plus the 3 commands to reproduce everything.

## Order

L4 (now, offline) → L5 + L3 on OpenJev (background) → L1 as keys arrive → L2 once NVIDIA is available (needs a strong attacker *and* a separate-family verifier) → L7 → update REPORT, push.

## Phase 3: Screener evaluation protocol (frozen 2026-10-24, before any run below)

Written before running anything in this section, and committed so the git history shows it came first. Motivated by
fellowship review feedback and by two practices in Antoniades et al. 2026 (*Heuresis*, arXiv:2606.25198): treat
the judge as a measured component with a fixed regression suite, and score on held-out data, because a method
that ranks first on the data it was built on can fail elsewhere.

**Disclosure.** The v1 evaluation (`results/screener_eval.md`) already ran the Screener on all 120 items. The
Screener's prompt, K = 3 and the escalation rule (spread >= 2 or median = 3) were fixed before that run and are
not changed here. Any *new* component (the heading-less segmenter below) is developed on the dev split only.

**Split.** By system, since the five sections of a technical file share a system: dev = AIReg-Bench uses 1-4
(60 items, 37 expert non-compliant), test = uses 5-8 (60 items, 36). Test is run once per frozen configuration.

**Document conditions** (target excerpt first in a five-section file, as in v1):
- `headed`: sections start with `**Article N**` (the v1 condition).
- `titled`: each `Article N` heading line replaced by a plain section title (`## 1. Human oversight`), no Article
  numbers, like many real Annex IV files.
- `plain`: heading lines and section separators removed; one continuous text.

**Methods**
- `whole_nano` (x3 reps): one whole-file Nemotron 3 Nano call, AIReg-Bench prompt. Reported per rep and as the
  median of the three (a compute-matched majority vote).
- `whole_ultra` (x1): one whole-file Nemotron 3 Ultra call, AIReg-Bench prompt (the bigger-model baseline).
- `section_nano1`, `section_nano3` (ablations, read from the Screener's own samples): first sample only; median of
  three without escalation.
- `screener` (x3 reps on `headed`, x1 on `titled` and `plain`): the full pipeline. On `titled`/`plain` it is run
  as shipped (whole-text fallback) and with the segmenter (`screener_seg`).

**Metrics.** Primary: false clearance on expert non-compliant items (median expert score < 4), counted two ways:
score >= 4 (comparable across methods) and, for the Screener, a confident "likely compliant" verdict. Secondary:
QWK and MAE vs the expert median, false rejection on expert-compliant items, human-review rate, model calls per
item. Uncertainty: paired item bootstrap (10,000 resamples, 95% percentile CI) for every method difference;
cluster bootstrap over the 8 systems as a sensitivity check; mean and SD across reps.

**Decision rule.** "The Screener reduces false clearance relative to X" is claimed only if the paired 95% CI of the
difference excludes 0 on the test split. Results that miss this are reported as they are.

**Regression suite** (`screener/regression.py`): a fixed list of cases with an expected outcome (unanimous-expert
violations must not be cleared, unanimous-expert compliant files must not be rejected, injected reviewer notes
must be flagged, heading-less files must still be split). Run before and after any engine change; per-case table
committed with the results.

### Phase 3 log (dev split only)

- 2026-10-24, segmenter v1 (Nano labels every paragraph): Nano returned 39 labels for a 95-paragraph file, so most
  text was dropped. Discarded. Its 77 partial dev rows are kept in
  `results/screener_eval_v2_discarded_label_segmenter.jsonl` and are not reported.
- Segmenter v2 (model names where each Article's section starts; sections run to the next start), on 20 dev
  files (10 items x titled/plain): full target section recovered 11/20 with Nano, 20/20 with Ultra.
  **Frozen: v2 with Nemotron 3 Ultra** (one extra call per heading-less file). Test split not touched before this.
