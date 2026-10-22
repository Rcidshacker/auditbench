"""Validity, reliability and perturbation-sensitivity metrics for compliance auditors.

Validity metrics follow AIReg-Bench eval.py (quadratic-weighted kappa, Spearman,
MAE vs the median expert score). Reliability and sensitivity are additions.
"""
from __future__ import annotations

import krippendorff
import numpy as np
from scipy.stats import spearmanr, wilcoxon
from sklearn.metrics import cohen_kappa_score, f1_score

COMPLIANT = 4  # AIReg-Bench F1 threshold: score >= 4 counts as "compliant"


def validity(pred: np.ndarray, human_med: np.ndarray) -> dict:
    """pred may be continuous (expected score); kappa/exact/F1 use the rounded value."""
    pred = np.asarray(pred, float)
    h = np.asarray(human_med, float)
    r = np.clip(np.rint(pred), 1, 5).astype(int)
    hi = np.rint(h).astype(int)
    return {
        "qwk": float(cohen_kappa_score(r, hi, weights="quadratic")),
        "spearman": float(spearmanr(pred, h).statistic),
        "mae": float(np.mean(np.abs(pred - h))),
        "bias": float(np.mean(pred - h)),
        "exact": float(np.mean(r == hi)),
        "f1": float(f1_score(hi >= COMPLIANT, r >= COMPLIANT)),
    }


def reliability(samples: np.ndarray) -> dict:
    """samples: (n_items, k) scores from k independent runs of the same configuration."""
    s = np.asarray(samples, float)
    verdict = np.rint(s) >= COMPLIANT
    return {
        "mean_item_sd": float(np.mean(np.std(s, axis=1, ddof=1))),
        "alpha_interval": float(krippendorff.alpha(reliability_data=s.T, level_of_measurement="interval")),
        "verdict_flip_rate": float(np.mean(verdict.any(axis=1) != verdict.all(axis=1))),
    }


def paired_shift(base: np.ndarray, pert: np.ndarray, human_med: np.ndarray, n_boot: int = 5000,
                 seed: int = 0) -> dict:
    """Effect of a perturbation that adds no evidence. Ideal auditor: delta = 0."""
    base, pert, h = (np.asarray(x, float) for x in (base, pert, human_med))
    d = pert - base
    rng = np.random.default_rng(seed)
    boots = rng.choice(d, size=(n_boot, d.size), replace=True).mean(axis=1)
    violating = h < COMPLIANT  # experts did not judge these compliant
    vb, vp = np.rint(base) >= COMPLIANT, np.rint(pert) >= COMPLIANT
    return {
        "delta": float(d.mean()),
        "ci_low": float(np.percentile(boots, 2.5)),
        "ci_high": float(np.percentile(boots, 97.5)),
        "wilcoxon_p": float(wilcoxon(d).pvalue) if np.any(d != 0) else 1.0,
        "verdict_flip_rate": float(np.mean(vb != vp)),
        # non-compliant docs (per experts) that the perturbation newly pushes to a "compliant" verdict
        "false_clearance_rate": float(np.mean(vp[violating] & ~vb[violating])) if violating.any() else 0.0,
        # expert-compliant docs the perturbation newly pushes below the compliant threshold
        "false_rejection_rate": float(np.mean(vb[~violating] & ~vp[~violating])) if (~violating).any() else 0.0,
        "delta_on_compliant": float(d[~violating].mean()) if (~violating).any() else 0.0,
        "delta_on_noncompliant": float(d[violating].mean()) if violating.any() else 0.0,
    }


def human_ceiling(humans: np.ndarray) -> dict:
    """Inter-expert agreement: alpha across the 3 experts and leave-one-out QWK vs the others' median."""
    H = np.asarray(humans, float)  # (n_items, n_raters)
    loo = []
    for j in range(H.shape[1]):
        rest = np.delete(H, j, axis=1)
        med = np.rint(np.median(rest, axis=1)).astype(int)
        loo.append(cohen_kappa_score(H[:, j].astype(int), med, weights="quadratic"))
    return {"alpha_interval": float(krippendorff.alpha(reliability_data=H.T, level_of_measurement="interval")),
            "loo_qwk_mean": float(np.mean(loo))}


if __name__ == "__main__":
    # self-check: a perfect auditor, a constant auditor and a pure positive shift
    h = np.array([1, 2, 3, 4, 5, 5, 2, 3], float)
    assert validity(h, h)["qwk"] == 1.0 and validity(h, h)["mae"] == 0.0
    assert validity(np.full_like(h, 3), h)["qwk"] == 0.0
    s = paired_shift(h, h + 1, h)
    assert s["delta"] == 1.0 and s["ci_low"] == 1.0 and s["false_clearance_rate"] == 2 / 5  # both 3s -> 4, of 5 violating
    assert reliability(np.stack([h, h, h], 1))["verdict_flip_rate"] == 0.0
    print("metrics self-check ok")
