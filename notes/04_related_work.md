# Related work the project builds on

Abstracts verified against the arXiv API on 2026-10-22.

## Direct foundation

**AIReg-Bench** (Marino et al., arXiv:2510.01474, Oct 2025). *Merlin Stein's "related reading" for the Automating AI Governance stream.*
- What it is: 120 LLM-generated technical-documentation excerpts for fictional high-risk systems (8 Annex III uses × Arts 9/10/12/14/15 × {compliant, violation 1, violation 2}).
- Labels: three legal experts score compliance 1–5. Frontier LLMs score the same excerpts with a fixed prompt. Metrics are QWK, Spearman, MAE and F1 vs the median expert.
- Our recomputation from their spreadsheets: Gemini 2.5 Pro QWK 0.863, GPT-5 0.849, Grok 4 0.829 … o3-mini 0.624. Expert inter-rater α = 0.657.
- Gaps it leaves open: **one sample per item** (no test–retest), **no robustness tests** (its prompt tells judges to "ignore any self-assessment", but never checks whether they do), only a holistic score.
- Repo: github.com/camlsys/aireg-bench. **No licence file**: used here for research evaluation only, not redistributed.

## Same mentor, same question one level up

**Audit tools of the trade** (Slater, Lundqvist, Richter, Wei; arXiv:2610.16911, 12 Oct 2026; a Pivotal fellowship output mentored by Kevin Wei).
- Setup: Petri auditing coding agents. Adding context to the auditor (an external codebase, benchmark transcripts, even just a benchmark abstract) shifted measured reward hacking a lot, e.g. 1.7 → 6.1 on a 1–10 scale.
- Conclusion: "measured rate of target behaviour is highly sensitive to configuration decisions."
- **How we extend it:** the same question (*does auditor context change the verdict?*) for *regulatory compliance* auditors, with expert ground truth, so we can separate "the score moved" from "the score got worse".

**Simpler Is Better for Autograders** (Dev, Paskov, Sloan, **Wei** et al., RAND RR-A4618-1, Apr 2026). A simple rubric autograder beat more complex LLM grading pipelines. Our holistic vs decomposed comparison tests this claim in the compliance domain.

**Human Baselines in Model Evaluations Need Rigor and Transparency** (**Wei**, Paskov et al., ICML 2025 position paper + reporting checklist). We report the expert-agreement ceiling next to every model number for this reason.

**Public vs Private Bodies: Who Should Run Advanced AI Evaluations and Audits?** (**Stein**, Gandhi, Kriecherbauer, Oueslati, Trager; AIES 2024). Argues audits need independence, expertise and access. Automated auditors are one way to scale that capacity, which raises the reliability question.

## Judge reliability literature

**Reliability without Validity** (Norman, Rivera, Hughes; arXiv:2606.19544, Jun 2026).
- Setup: 21 judges, ~541k judgments.
- Findings: exact-match overstates agreement by 33–41 pp vs κ, and a judge can be highly test–retest consistent (>0.95) yet badly biased. They propose a Minimum Viable Validation Protocol.
- **How we use it:** report κ (not just exact match), and measure consistency *and* bias (perturbation shift) separately.

## Oversight / monitoring neighbours

**Democratizing Agent Deployment Safety: A Structural Monitoring Approach** (Ravindra, Tiwari, Wolowski; arXiv:2607.14570). Untrained structural (information-flow-graph) monitors for coding-agent sabotage in ControlArena. Relevant if pitching to Jess Bergs / Preeti Ravindra.

## Incident context

- **Hugging Face incident** (Jul 2026). Investigation by METR + Redwood: metr.org/hugging-face-incident-report-aug-2026.pdf. Overview at 80000hours.org/hugging-face.
- Why it matters here: the incident pushes regulators toward faster, automated assurance, so the reliability of automated auditors becomes a load-bearing question.
