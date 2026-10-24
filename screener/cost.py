"""Tokens and dollar cost per Article judgement: the Screener vs one whole-file Nemotron 3 Ultra call.

Measured on 20 AIReg-Bench items (seeded random sample, both splits), each placed first in a five-section technical file, as
in the v2 evaluation. Prices are Token Factory list prices from its /v1/models endpoint (2026-10-24).

    python -m screener.cost        # writes results/cost.md
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from auditbench import providers
from auditbench.data import load_items

from .engine import FAST, STRONG, assess_article, split_sections
from .evaluate import build, whole

RES = Path(__file__).resolve().parent.parent / "results"
PRICE = {FAST.split(":", 1)[1]: (0.06, 0.24), STRONG.split(":", 1)[1]: (1.00, 3.00)}  # USD per 1M tokens in, out


def measure(fn) -> dict:
    """Run fn in isolation and total the tokens and cost of the calls it made."""
    providers.USAGE.clear()
    t0 = time.time()
    fn()
    secs = time.time() - t0
    tin = tout = cost = 0.0
    for model, u in providers.USAGE:
        i, o = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        tin, tout = tin + i, tout + o
        cost += (i * PRICE[model][0] + o * PRICE[model][1]) / 1e6
    return {"in": tin, "out": tout, "usd": cost, "calls": len(providers.USAGE), "secs": secs}


def main():
    all_items = load_items()  # every 6th item would pick only "compliant" variants
    items = [all_items[i] for i in np.random.default_rng(0).choice(len(all_items), 20, replace=False)]
    rows = {"screener": [], "ultra": []}
    for it in items:  # sequential, so USAGE holds only this measurement's calls
        doc = build(it, "headed")
        sec = split_sections(doc)[it.article]
        rows["screener"].append(measure(lambda: assess_article(it.article, sec, it.system_outline)))
        rows["ultra"].append(measure(lambda: whole(STRONG, it, doc)))
        print(it.item_id, {k: round(v[-1]["usd"], 5) for k, v in rows.items()})
    md = ["# Cost per Article judgement (20 items, five-section files, Token Factory list prices)", "",
          "| method | calls | input tokens | output tokens | USD per Article | USD per 5-Article file | wall time per Article |",
          "|---|---|---|---|---|---|---|"]
    for name, label in (("ultra", "One whole-file Nemotron 3 Ultra call"), ("screener", "AuditBench Screener")):
        r = rows[name]
        m = {k: float(np.mean([x[k] for x in r])) for k in ("calls", "in", "out", "usd", "secs")}
        md.append(f"| {label} | {m['calls']:.2f} | {m['in']:,.0f} | {m['out']:,.0f} | ${m['usd']:.5f} | "
                  f"${5 * m['usd']:.4f} | {m['secs']:.1f} s |")
    esc = np.mean([x["calls"] > 3 for x in rows["screener"]])
    ratio = np.mean([x["usd"] for x in rows["ultra"]]) / np.mean([x["usd"] for x in rows["screener"]])
    md += ["", f"Escalated to Ultra on {esc:.0%} of this sample (v2 evaluation: 38%). Whole-file Ultra costs {ratio:.1f}x the Screener per Article. Prices (USD per 1M tokens, in/out): "
               f"Nano 0.06/0.24, Ultra 1.00/3.00. A 5-Article file needs 5 judgements either way. Wall time is one "
               "sequential measurement from India and includes network latency."]
    (RES / "cost.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
