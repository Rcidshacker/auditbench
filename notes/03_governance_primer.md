# AI governance primer: what the PDF roadmap covers, condensed

Source: "AI Governance & Ethics Roadmap 2026" (the PDF) plus primary texts. EU AI Act wording comes from the Article extracts in `external/aireg-bench/articles.txt`. Timeline facts are from the European Commission AI Act page and FPF (checked 2026-10-22).

## 1. Four terms people mix up

| Term | Question it answers |
|---|---|
| AI ethics | What *should* AI systems do? (values) |
| Responsible AI | How does an organisation turn those values into practice? |
| AI governance | Which policies, processes, controls and institutions decide how AI is built and used? |
| AI safety | How do we stop increasingly capable systems from causing serious harm? |

## 2. Principle frameworks (the "what")

- **OECD AI Principles** (2019, updated 2024): inclusive growth and well-being; human rights and democratic values (fairness, privacy); transparency and explainability; robustness, security and safety; accountability. The most-cited practical starting point.
- **UNESCO Recommendation on the Ethics of AI** (2021): human-rights-centred. Its principles include proportionality/do-no-harm, safety and security, privacy, multi-stakeholder governance, responsibility and accountability, transparency and explainability, human oversight and determination, sustainability, awareness/literacy, fairness and non-discrimination.

## 3. NIST AI RMF (the "how", risk management)

- **AI RMF 1.0** (NIST AI 100-1, Jan 2023): voluntary, sector-agnostic, no certification. Still the current core in 2026. NIST extends it through *profiles*, not version numbers.
- Four functions:
  - **GOVERN** (cross-cutting): who is accountable? Policies, culture, third-party oversight.
  - **MAP** (per system): context, intended purpose, stakeholders, risks.
  - **MEASURE**: test and track risks with metrics. This is the step most organisations skip, and it's where an *auditor benchmark* lives.
  - **MANAGE**: treat, monitor, respond to incidents.
- **Generative AI Profile** (NIST AI 600-1, Jul 2024): 12 GAI risks. CBRN information; confabulation; dangerous/violent content; data privacy; environmental impact; harmful bias/homogenisation; human-AI configuration; information integrity; information security; intellectual property; obscene/abusive content; value chain and component integration. Each risk maps to suggested actions per RMF subcategory (e.g. `GV-1.1-001`).

## 4. EU AI Act (the "must", regulation)

**Risk tiers.**
- Prohibited practices (Art 5; the Omnibus added a ban on non-consensual sexual deepfakes).
- **High-risk** (Art 6 + Annex III areas: biometrics, critical infrastructure, education, employment, essential services/credit, law enforcement, migration/border, justice/democracy).
- Transparency obligations (Art 50: chatbots, deepfakes, AI-generated content).
- Minimal risk.
- Separately, **GPAI models** (Arts 51–55; systemic-risk models get extra duties; Code of Practice).

**Roles.** The *provider* develops and places the system on the market and carries most Arts 9–17 duties. The *deployer* uses it professionally (Art 26: use per instructions, human oversight, monitoring, logs, informing workers).

**Arts 9–15, the provider requirements AIReg-Bench tests:**

| Art | Requirement, in one line | Typical failure a documentation auditor should catch |
|---|---|---|
| 9 Risk management | A continuous, iterative, documented lifecycle process: identify, estimate and evaluate risks (incl. foreseeable misuse), adopt targeted measures, test against defined metrics, consider minors/vulnerable groups | Risk process is one-off, ignores misuse, has no test thresholds |
| 10 Data governance | Training/validation/test data under governance practices: relevant, representative, error-free "to the best extent possible", bias examination and mitigation, documented provenance and gaps | No bias examination; unrepresentative data waved through |
| 12 Record-keeping | Automatic event logging over the lifetime, enough for traceability, post-market monitoring and risk identification | Logging off by default, not tamper-evident, missing key events |
| 14 Human oversight | Designed so natural persons can understand, monitor, interpret and override/stop the system; measures proportional to risk; guards against automation bias | "Human in the loop" in name only; no stop button; no automation-bias training |
| 15 Accuracy, robustness, cybersecurity | Appropriate, declared accuracy levels; resilience to errors and feedback loops; protection against data poisoning, adversarial examples, model flaws | Accuracy undeclared; no adversarial testing; feedback-loop bias |

**Timeline after the AI Omnibus** (published OJ 24 Jul 2026, in force 27 Jul 2026):
- Prohibitions + AI literacy: 2 Feb 2025
- GPAI rules: 2 Aug 2025
- Art 50 transparency: 2 Aug 2026 (50(2) content marking: 2 Dec 2026)
- **Annex III high-risk: 2 Dec 2027**
- Annex I product-embedded: 2 Aug 2028
- Draft high-risk classification guidelines: 19 May 2026

Why it matters for this project: there's a ~13-month window before Arts 9–15 bite, and notified bodies and providers will reach for LLM tooling to pre-screen technical documentation. Whether such tools are *reliable and manipulation-resistant* is an open, time-sensitive question.

## 5. Practitioner artefacts the roadmap asks for (and where this folder covers them)

| Roadmap artefact | Covered by |
|---|---|
| AI risk register | §6 of `REPORT.md`: risk register for *LLM compliance auditors* (the system under study) |
| NIST AI RMF case study | `REPORT.md` §6 maps findings to GOVERN/MAP/MEASURE/MANAGE |
| EU AI Act checklist | Table in §4 above + the decomposed auditor's per-paragraph questions (`auditbench/auditors.py`) |
| Red-team report | The perturbation suite *is* a red-team of the auditor (assurance, authority injection, negative sentiment, reformatting) |
| Policy memo | `REPORT.md` §7: recommendations for regulators/notified bodies using LLM pre-screening |

## 6. Learning path still worth doing (free, in order)

1. Microsoft "Explore Responsible AI" (34 min)
2. UNESCO Ethics of AI MOOC (~10 h)
3. NIST AI RMF Playbook, skimming the Measure section
4. EU AI Act official overview + AI Office Service Desk timeline
5. BlueDot AI Governance course (the cohort network matters for this field)
6. IAPP AIGP body of knowledge (only if pursuing compliance roles)
