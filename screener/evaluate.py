"""Does the Screener fix the long-file blind spot? Evaluated on Nebius Token Factory.

For each of the 120 expert-labelled AIReg-Bench items, the target excerpt is placed FIRST in a five-section
technical file (the condition where whole-file judges falsely cleared up to 15% of non-compliant documents).
  baseline: one whole-file call to Nemotron 3 Nano with AIReg-Bench's own prompt
  screener: the Screener pipeline (section split, 3 Nano samples, Ultra escalation) on the target Article

    python -m screener.evaluate            # resumable; writes results/screener_eval.jsonl and screener_eval.md
"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from auditbench.auditors import generative_prompt, parse_generative
from auditbench.data import load_items
from auditbench.metrics import validity
from auditbench.providers import generate
from auditbench.stress import dossier

from .engine import FAST, assess_article, split_sections

RES = Path(__file__).resolve().parent.parent / "results"
OUT = RES / "screener_eval.jsonl"


def one(it) -> dict:
    doc = dossier(it, "first")
    text, model, _ = generate(FAST, generative_prompt(it, "dossier_first"))
    base = parse_generative(text)["score"]
    sec = split_sections(doc).get(it.article)
    if sec is None:
        raise RuntimeError(f"section split missed Article {it.article}")
    s = assess_article(it.article, sec, it.system_outline)
    return {"item_id": it.item_id, "baseline": base, "screener": s["score"], "verdict": s["verdict"],
            "fast_scores": s["fast_scores"], "escalated": s["escalated"]}


def main():
    items = load_items()
    done = {json.loads(l)["item_id"] for l in OUT.read_text(encoding="utf-8").splitlines()} if OUT.exists() else set()
    todo = [it for it in items if it.item_id not in done]
    print(f"{len(todo)} items to evaluate")
    with ThreadPoolExecutor(6) as ex, OUT.open("a", encoding="utf-8") as f:
        for it, fut in [(it, ex.submit(one, it)) for it in todo]:
            try:
                f.write(json.dumps(fut.result()) + "\n")
                f.flush()
            except Exception as e:
                print("FAIL", it.item_id, str(e)[:150])
    report(items)


def report(items):
    rows = {r["item_id"]: r for r in map(json.loads, OUT.read_text(encoding="utf-8").splitlines())}
    its = [it for it in items if it.item_id in rows]
    h = np.array([it.human_median for it in its])
    nonc = h < 4
    md = ["# Screener vs whole-file judge on Nebius Token Factory", "",
          f"{len(its)}/120 AIReg-Bench items; each target excerpt placed first in a 5-section technical file.", "",
          "| method | QWK vs experts | MAE | false clearance (expert non-compliant judged ≥4) | needs-review rate |",
          "|---|---|---|---|---|"]
    for name in ("baseline", "screener"):
        s = np.array([rows[it.item_id][name] for it in its], float)
        v = validity(s, h)
        fc = float(np.mean(np.rint(s[nonc]) >= 4))
        review = (f"{np.mean([rows[it.item_id]['verdict'] == 'needs human review' for it in its]):.1%}"
                  if name == "screener" else "n/a")
        label = "Whole-file Nemotron 3 Nano (AIReg-Bench prompt)" if name == "baseline" else \
            "AuditBench Screener (per-section, 3× Nano + Ultra escalation)"
        md.append(f"| {label} | {v['qwk']:.3f} | {v['mae']:.3f} | {fc:.1%} ({int(np.sum(np.rint(s[nonc]) >= 4))}/"
                  f"{int(nonc.sum())}) | {review} |")
    esc = np.mean([rows[it.item_id]["escalated"] for it in its])
    md += ["", f"Escalated to Nemotron 3 Ultra on {esc:.0%} of items."]
    (RES / "screener_eval.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md).encode("ascii", "replace").decode())


if __name__ == "__main__":
    main()
