"""L4: how much of the headline survives ground-truth noise? Writes results/L4_ground_truth.md.

- paired bootstrap CI on QWK differences between auditors (same items resampled together)
- agreement with each individual expert, not only the median
- validity on the high-agreement subset (experts' scores span <= 1 point)
- AUROC against the generation-intent label (compliant file vs violation file)
"""
from __future__ import annotations

import json
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import cohen_kappa_score, roc_auc_score

from .data import BASELINE_MODELS, load_items, load_llm_baseline
from .metrics import validity

warnings.filterwarnings("ignore")
RES = Path(__file__).resolve().parent.parent / "results"


def qwk(pred, h) -> float:
    return float(cohen_kappa_score(np.clip(np.rint(pred), 1, 5).astype(int), np.rint(h).astype(int),
                                   weights="quadratic"))


def paired_qwk_diff(a, b, h, n_boot=5000, seed=0) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(h)
    diffs = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        diffs.append(qwk(a[i], h[i]) - qwk(b[i], h[i]))
    return qwk(a, h) - qwk(b, h), float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def auditor_scores(items) -> dict[str, np.ndarray]:
    """Unperturbed score per item for our auditors (mean over samples) and published single runs."""
    ids = [it.item_id for it in items]
    cell = defaultdict(lambda: defaultdict(list))
    for f in sorted(RES.glob("runs*.jsonl")):
        for r in map(json.loads, f.read_text(encoding="utf-8").splitlines()):
            if r["perturbation"] == "none":
                cell[r["config"]][r["item_id"]].append(r["score"])
    out = {f"ours:{c}": np.array([np.mean(d[i]) for i in ids]) for c, d in cell.items() if all(d.get(i) for i in ids)}
    for m in BASELINE_MODELS:
        b = load_llm_baseline(m, items)
        out[f"published:{m}"] = np.array([b[i] for i in ids])
    return out


def table(rows, cols) -> str:
    f = lambda v: f"{v:.3f}" if isinstance(v, float) else str(v)
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)] +
                     ["| " + " | ".join(f(r.get(c, "")) for c in cols) + " |" for r in rows])


def main():
    items = load_items()
    H = np.array([it.human for it in items])  # (n, 3)
    hmed = np.median(H, axis=1)
    intent = np.array([it.variant == "compliant" for it in items])
    S = auditor_scores(items)
    ref = S["ours:holistic"]

    md = ["# L4: ground-truth noise", ""]

    rows = []
    for name, s in sorted(S.items(), key=lambda kv: -qwk(kv[1], hmed)):
        d, lo, hi = paired_qwk_diff(ref, s, hmed) if name != "ours:holistic" else (0.0, 0.0, 0.0)
        rows.append({"auditor": name, "qwk": qwk(s, hmed), "holistic_minus_this": d, "ci_low": lo, "ci_high": hi,
                     "significant": "yes" if (lo > 0 or hi < 0) else "no"})
    md += ["## Is the gap real? Paired bootstrap of QWK(ours:holistic) − QWK(auditor), 5,000 resamples", "",
           table(rows, ["auditor", "qwk", "holistic_minus_this", "ci_low", "ci_high", "significant"]), ""]

    rows = []
    for name, s in S.items():
        per = [qwk(s, H[:, j]) for j in range(3)]
        rows.append({"auditor": name, "expert_1": per[0], "expert_2": per[1], "expert_3": per[2],
                     "min": min(per), "max": max(per)})
    for j in range(3):  # each expert against the other two experts' mean, as a human reference
        others = np.delete(H, j, axis=1).mean(1)
        rows.append({"auditor": f"human: expert {j + 1} vs others' mean", **{f"expert_{k + 1}": "" for k in range(3)},
                     "min": qwk(H[:, j], others), "max": qwk(H[:, j], others)})
    md += ["## Agreement with each expert separately (QWK)", "", table(rows, ["auditor", "expert_1", "expert_2",
                                                                              "expert_3", "min", "max"]), ""]

    agree = (H.max(1) - H.min(1)) <= 1
    rows = [{"auditor": n, "n": int(agree.sum()), **validity(s[agree], hmed[agree])} for n, s in S.items()]
    rows.sort(key=lambda r: -r["qwk"])
    md += [f"## High-agreement subset (experts span ≤ 1 point): {int(agree.sum())}/{len(items)} items", "",
           table(rows, ["auditor", "n", "qwk", "mae", "f1"]), ""]

    rows = [{"auditor": n, "auroc_vs_intent": float(roc_auc_score(intent, s)),
             "auroc_vs_expert_median": float(roc_auc_score(hmed >= 4, s))} for n, s in S.items()]
    rows.append({"auditor": "human: expert median", "auroc_vs_intent": float(roc_auc_score(intent, hmed)),
                 "auroc_vs_expert_median": ""})
    rows.sort(key=lambda r: -r["auroc_vs_intent"])
    md += ["## AUROC: separating compliant from violation documents", "",
           "`auroc_vs_intent` uses which file the item came from (compliant vs violation), a label independent of "
           "the experts.", "", table(rows, ["auditor", "auroc_vs_intent", "auroc_vs_expert_median"]), ""]

    (RES / "L4_ground_truth.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
