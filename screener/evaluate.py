"""Phase-3 Screener evaluation on Nebius Token Factory, per the frozen protocol in PLAN.md.

Each of the 120 expert-labelled AIReg-Bench items is placed FIRST in a five-section technical file, in three
document conditions (headed / titled / plain), and judged by whole-file baselines and by the Screener.
v1 results (results/screener_eval.md) are kept as they were.

    python -m screener.evaluate --split dev --stage seg     # develop the segmenter on dev only
    python -m screener.evaluate --split test --stage all    # frozen configs on test, once
    python -m screener.evaluate --report                    # rebuild results/screener_eval_v2.md
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from auditbench.auditors import _AIREG, parse_generative
from auditbench.data import ARTICLES, Item, load_items
from auditbench.metrics import validity
from auditbench.providers import generate
from auditbench.stress import _compliant_excerpt, dossier

from .engine import FAST, STRONG, TITLES, assess_article, segment, split_sections

RES = Path(__file__).resolve().parent.parent / "results"
OUT = RES / "screener_eval_v2.jsonl"
DEV_USES = {1, 2, 3, 4}  # test = uses 5-8 (PLAN.md, phase 3)
_HEAD = re.compile(r"(?im)^[#*>_ \t-]*article\s+\d+\b[^\n]{0,40}$\n?")


def build(it: Item, cond: str) -> str:
    """The item's excerpt first, then the compliant excerpts for the other four Articles of the same system."""
    if cond == "headed":
        return dossier(it, "first")
    parts = [(it.article, it.documentation)] + [(a, _compliant_excerpt(a, it.use, it.system))
                                               for a in ARTICLES if a != it.article]
    if cond == "titled":
        return "\n\n".join(f"## {k}. {TITLES[a]}\n\n{_HEAD.sub('', t).strip()}" for k, (a, t) in enumerate(parts, 1))
    return "\n\n".join(_HEAD.sub("", t).strip() for _, t in parts)  # plain


def whole(model: str, it: Item, doc: str) -> dict:
    text, _, _ = generate(model, _AIREG["build_prompt"](it.article_text, doc, it.system_outline, it.article, 0))
    return {"score": parse_generative(text)["score"], "calls": 1}


def screener(it: Item, doc: str, seg: bool) -> dict:
    sec, seg_found, calls = split_sections(doc).get(it.article), None, 0
    if sec is None and seg:
        sections, calls = segment(doc), 1
        sec = sections.get(it.article)
        seg_found = sec is not None
        # did the segmenter put the target excerpt (its last line) into the target section?
        seg_found = seg_found and it.documentation.strip().splitlines()[-1][:80] in sec
    s = assess_article(it.article, sec or doc, it.system_outline)
    return {"score": s["score"], "verdict": s["verdict"], "fast_scores": s["fast_scores"],
            "escalated": s["escalated"], "seg_found": seg_found, "whole_text": sec is None,
            "calls": calls + len(s["fast_scores"]) + int(s["escalated"])}


METHODS = {"whole_nano": lambda it, doc: whole(FAST, it, doc),
           "whole_ultra": lambda it, doc: whole(STRONG, it, doc),
           "screener": lambda it, doc: screener(it, doc, seg=False),
           "screener_seg": lambda it, doc: screener(it, doc, seg=True)}

# (cond, method, reps) per stage; frozen in PLAN.md
STAGES = {"base": [("headed", "whole_nano", 3), ("headed", "whole_ultra", 1), ("headed", "screener", 3),
                   ("plain", "whole_nano", 1), ("plain", "whole_ultra", 1),
                   ("titled", "screener", 1), ("plain", "screener", 1)],
          "seg": [("titled", "screener_seg", 1), ("plain", "screener_seg", 1)]}
STAGES["all"] = STAGES["base"] + STAGES["seg"]


def run(split: str, stage: str, workers: int):
    items = [it for it in load_items() if split == "all" or (it.use in DEV_USES) == (split == "dev")]
    done = {(r["item_id"], r["cond"], r["method"], r["rep"]) for r in _rows()}
    jobs = [(it, c, m, r) for c, m, reps in STAGES[stage] for r in range(reps) for it in items
            if (it.item_id, c, m, r) not in done]
    print(f"{len(jobs)} jobs ({split}, {stage})")

    def one(job):
        it, c, m, r = job
        return {"item_id": it.item_id, "cond": c, "method": m, "rep": r, **METHODS[m](it, build(it, c))}

    with ThreadPoolExecutor(workers) as ex, OUT.open("a", encoding="utf-8") as f:
        for job, fut in [(j, ex.submit(one, j)) for j in jobs]:
            try:
                f.write(json.dumps(fut.result()) + "\n")
                f.flush()
            except Exception as e:
                print("FAIL", job[0].item_id, job[1], job[2], str(e)[:150])


def _rows() -> list[dict]:
    return [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines()] if OUT.exists() else []


def _boot_ci(x: np.ndarray, n: int = 10_000, seed: int = 0, clusters: np.ndarray | None = None):
    """95% percentile CI of mean(x); item bootstrap, or cluster bootstrap over `clusters`."""
    rng = np.random.default_rng(seed)
    if clusters is None:
        b = rng.choice(x, size=(n, x.size)).mean(axis=1)
    else:
        ids = np.unique(clusters)
        groups = [x[clusters == c] for c in ids]
        b = np.array([np.concatenate([groups[i] for i in rng.integers(0, len(ids), len(ids))]).mean()
                      for _ in range(n)])
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def report():
    items = {it.item_id: it for it in load_items()}
    rows = _rows()
    by = {}
    for r in rows:
        by.setdefault((r["cond"], r["method"]), {}).setdefault(r["item_id"], {})[r["rep"]] = r

    def series(cond, method, how):
        """item_id -> score for a method variant; None if any item lacks the needed reps."""
        d = by.get((cond, method), {})
        out = {}
        for iid, reps in d.items():
            r0 = reps.get(0)
            if how == "rep0":
                out[iid] = r0["score"]
            elif how == "median3":
                if len(reps) < 3:
                    continue
                out[iid] = statistics.median(reps[k]["score"] for k in range(3))
            elif how == "nano1":
                out[iid] = r0["fast_scores"][0]
            elif how == "nano3":
                out[iid] = statistics.median(r0["fast_scores"])
        return out

    variants = [  # label, cond, method, how
        ("Whole-file Nano, 1 call", "headed", "whole_nano", "rep0"),
        ("Whole-file Nano, median of 3", "headed", "whole_nano", "median3"),
        ("Whole-file Ultra, 1 call", "headed", "whole_ultra", "rep0"),
        ("Per-section Nano, 1 sample (ablation)", "headed", "screener", "nano1"),
        ("Per-section Nano, median of 3, no escalation (ablation)", "headed", "screener", "nano3"),
        ("Screener (full)", "headed", "screener", "rep0"),
        ("Whole-file Nano, 1 call", "plain", "whole_nano", "rep0"),
        ("Whole-file Ultra, 1 call", "plain", "whole_ultra", "rep0"),
        ("Screener as shipped (no headings found: whole text)", "titled", "screener", "rep0"),
        ("Screener + segmenter", "titled", "screener_seg", "rep0"),
        ("Screener as shipped (no headings found: whole text)", "plain", "screener", "rep0"),
        ("Screener + segmenter", "plain", "screener_seg", "rep0"),
    ]
    md = ["# Screener evaluation v2 (frozen protocol, PLAN.md phase 3)", "",
          "Nebius Token Factory. Each item's excerpt is placed first in a five-section technical file. False clearance "
          "(FC) = expert non-compliant item (median expert < 4) scored >= 4. False rejection (FR) = expert-compliant "
          "item scored <= 2. Brackets: 95% item-bootstrap CI.", ""]
    for split, uses in (("test", {5, 6, 7, 8}), ("dev", DEV_USES), ("all", set(range(1, 9)))):
        md += [f"## Split: {split}", "",
               "| condition | method | n | QWK | MAE | FC | FR | review rate | calls/item |", "|---|---|---|---|---|---|---|---|---|"]
        screener_fc = None
        diffs = []
        for label, cond, method, how in variants:
            s = series(cond, method, how)
            ids = [i for i in s if items[i].use in uses]
            if not ids:
                continue
            sc = np.array([s[i] for i in ids], float)
            h = np.array([items[i].human_median for i in ids])
            nonc = h < 4
            fc = (np.rint(sc) >= 4)[nonc].astype(float)
            fr = (np.rint(sc) <= 2)[~nonc].astype(float)
            v = validity(sc, h)
            reps = {i: by[(cond, method)][i] for i in ids}
            review = (f"{np.mean([reps[i][0].get('verdict') == 'needs human review' for i in ids]):.0%}"
                      if method.startswith("screener") and how == "rep0" else "")
            calls = {"rep0": np.mean([reps[i][0]["calls"] for i in ids]), "median3": 3.0, "nano1": 1.0,
                     "nano3": 3.0}[how]
            lo, hi = _boot_ci(fc)
            md.append(f"| {cond} | {label} | {len(ids)} | {v['qwk']:.3f} | {v['mae']:.2f} | {fc.mean():.1%} "
                      f"[{lo:.0%}, {hi:.0%}] ({int(fc.sum())}/{fc.size}) | {fr.mean():.1%} | {review} | {calls:.1f} |")
            if (cond, method, how) == ("headed", "screener", "rep0"):
                screener_fc = {i: float(np.rint(s[i]) >= 4) for i in ids if items[i].human_median < 4}
            diffs.append((cond, label, {i: float(np.rint(s[i]) >= 4) for i in ids if items[i].human_median < 4}))
        if screener_fc:
            md += ["", "Paired difference in FC vs the Screener (headed), on expert non-compliant items. Positive = the "
                   "other method clears more violations. Item and cluster (8 systems) bootstrap.", "",
                   "| condition | method | FC diff | 95% CI (item) | 95% CI (cluster) | excludes 0 (item) |",
                   "|---|---|---|---|---|---|"]
            for cond, label, d in diffs:
                common = [i for i in d if i in screener_fc]
                if (cond, label) == ("headed", "Screener (full)") or not common:
                    continue
                x = np.array([d[i] - screener_fc[i] for i in common])
                cl = np.array([items[i].use for i in common])
                lo, hi = _boot_ci(x)
                clo, chi = _boot_ci(x, clusters=cl)
                md.append(f"| {cond} | {label} | {x.mean():+.1%} | [{lo:+.1%}, {hi:+.1%}] | [{clo:+.1%}, {chi:+.1%}] | "
                          f"{'yes' if lo > 0 or hi < 0 else 'no'} |")
        md.append("")

    # rep-to-rep spread for the repeated configs (all items)
    md += ["## Run-to-run variation (headed, all items)", "", "| method | FC per rep | QWK per rep |", "|---|---|---|"]
    for label, method in (("Whole-file Nano", "whole_nano"), ("Screener", "screener")):
        d = by.get(("headed", method), {})
        fcs, qwks = [], []
        for k in range(3):
            ids = [i for i in d if k in d[i]]
            if not ids:
                continue
            sc = np.array([d[i][k]["score"] for i in ids], float)
            h = np.array([items[i].human_median for i in ids])
            fcs.append(f"{np.mean(np.rint(sc[h < 4]) >= 4):.1%}")
            qwks.append(f"{validity(sc, h)['qwk']:.3f}")
        md.append(f"| {label} | {', '.join(fcs)} | {', '.join(qwks)} |")

    seg = [r for r in rows if r["method"] == "screener_seg"]
    if seg:
        md += ["", "## Segmenter", "",
               f"Target section recovered (excerpt's last line inside the target section): "
               f"{np.mean([bool(r['seg_found']) for r in seg]):.0%} of {len(seg)} runs; target Article missing, "
               f"whole text used: {np.mean([r['whole_text'] for r in seg]):.0%}."]
    (RES / "screener_eval_v2.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md).encode("ascii", "replace").decode())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test", "all"], default="dev")
    ap.add_argument("--stage", choices=list(STAGES), default="base")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if not a.report:
        run(a.split, a.stage, a.workers)
    report()
