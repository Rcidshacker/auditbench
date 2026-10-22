"""Turn results/runs.jsonl into results/RESULTS.md (tables only, no prose)."""
from __future__ import annotations

import json
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np

from .data import BASELINE_MODELS, load_items, load_llm_baseline
from .metrics import human_ceiling, paired_shift, reliability, validity

warnings.filterwarnings("ignore")
RES = Path(__file__).resolve().parent.parent / "results"


def table(rows: list[dict], cols: list[str]) -> str:
    fmt = lambda v: f"{v:.3f}" if isinstance(v, float) else str(v)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(r.get(c, "")) for c in cols) + " |" for r in rows]
    return "\n".join(out)


def main():
    items = load_items()
    ids = [it.item_id for it in items]
    hmed = np.array([it.human_median for it in items])
    md = ["# AuditBench results", "", f"Items: {len(items)} AIReg-Bench excerpts (EU AI Act Arts 9, 10, 12, 14, 15).", ""]

    # 1. human ceiling and published frontier-model annotations
    hc = human_ceiling(np.array([it.human for it in items]))
    md += ["## 1. Reference points", "",
           f"Expert agreement: Krippendorff alpha (interval) = {hc['alpha_interval']:.3f}; "
           f"leave-one-expert-out QWK vs other experts' median = {hc['loo_qwk_mean']:.3f}.", ""]
    rows = []
    for m in BASELINE_MODELS:
        b = load_llm_baseline(m, items)
        v = np.array([b[i] for i in ids])
        ok = ~np.isnan(v)
        rows.append({"model": m, "n": int(ok.sum()), **validity(v[ok], hmed[ok])})
    rows.sort(key=lambda r: -r["qwk"])
    md += ["Published AIReg-Bench annotations (single sample, original prompt):", "",
           table(rows, ["model", "n", "qwk", "spearman", "mae", "bias", "exact", "f1"]), ""]

    # load our runs: cell[(config, perturbation)][item_id] -> list of scores over samples
    cell = defaultdict(lambda: defaultdict(list))
    cell_mean = defaultdict(lambda: defaultdict(list))
    lines = [ln for f in sorted(RES.glob("runs*.jsonl")) for ln in f.read_text(encoding="utf-8").splitlines()]
    for r in map(json.loads, lines):
        cell[(r["config"], r["perturbation"])][r["item_id"]].append(r["score"])
        if "score_mean" in r:
            cell_mean[("decomposed_meanagg", r["perturbation"])][r["item_id"]].append(r["score_mean"])
    cell.update(cell_mean)

    hmap = dict(zip(ids, hmed))

    def matrix(key, among=None):
        """(item ids, scores[n, k]) for items with the full k samples (k = most samples any item has)."""
        d = cell[key]
        have = [i for i in (among or ids) if d.get(i)]
        if not have:
            return [], None
        k = max(len(d[i]) for i in have)
        have = [i for i in have if len(d[i]) >= k]  # rate-limit gaps drop an item rather than shrink k
        return have, np.array([d[i][:k] for i in have])

    # 2. validity + reliability per configuration (unperturbed)
    rows = []
    for (c, p) in sorted(k for k in cell if k[1] == "none"):
        got, S = matrix((c, p))
        if S is None:
            continue
        h = np.array([hmap[i] for i in got])
        one = validity(S[:, 0], h)
        rows.append({"config": c, "n": len(got), "k": S.shape[1], **validity(S.mean(1), h),
                     "qwk_1sample": one["qwk"], **(reliability(S) if S.shape[1] > 1 else {})})
    md += ["## 2. Our auditors: validity vs experts and test-retest reliability", "",
           "qwk etc. use the mean over k independent samples; qwk_1sample uses only the first sample "
           "(comparable to the single-sample published numbers above).", "",
           table(rows, ["config", "n", "k", "qwk", "qwk_1sample", "spearman", "mae", "bias", "f1", "mean_item_sd",
                        "alpha_interval", "verdict_flip_rate"]), ""]

    # 3. perturbation sensitivity (paired on items present in both cells, per-item mean over samples)
    rows = []
    for (c, p) in sorted(k for k in cell if k[1] != "none"):
        got, _ = matrix((c, "none"))
        got, S = matrix((c, p), among=got)
        _, B = matrix((c, "none"), among=got)
        if S is None:
            continue
        h = np.array([hmap[i] for i in got])
        rows.append({"config": c, "perturbation": p, "n": len(got), **paired_shift(B.mean(1), S.mean(1), h)})
    md += ["## 3. Sensitivity to perturbations that add no evidence (ideal delta = 0)", "",
           "delta = mean(score_perturbed - score_original) on the 1-5 scale; 95% bootstrap CI; "
           "false_clearance = share of expert-non-compliant items newly rated compliant.", "",
           table(rows, ["config", "perturbation", "n", "delta", "ci_low", "ci_high", "wilcoxon_p",
                        "verdict_flip_rate", "false_clearance_rate", "false_rejection_rate", "delta_on_compliant",
                        "delta_on_noncompliant"]), ""]

    # 4. per-article breakdown for each unperturbed configuration
    art_of = {it.item_id: it.article for it in items}
    rows = []
    for (c, p) in sorted(k for k in cell if k[1] == "none"):
        got, S = matrix((c, p))
        if S is None:
            continue
        for art in sorted(set(art_of.values())):
            m = np.array([art_of[i] == art for i in got])
            if m.sum() < 2:  # partial runs can leave an Article empty
                continue
            h = np.array([hmap[i] for i in got])[m]
            rows.append({"config": c, "article": art, "n": int(m.sum()), **validity(S.mean(1)[m], h)})
    md += ["## 4. By Article", "", table(rows, ["config", "article", "n", "qwk", "mae", "bias", "f1"]), ""]

    (RES / "RESULTS.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
