"""Fixed regression suite for the Screener (PLAN.md phase 3): the judge is a measured component, so every engine
change is replayed against the same cases with a known expected outcome. Runs the full app pipeline (`screen`).

Cases use only items all three experts agree on (all scores <= 2, or all >= 4), one per Article per kind.

    python -m screener.regression        # writes results/regression.md; exit code 1 if any case fails
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from auditbench.auditors import apply
from auditbench.data import load_items

from .engine import screen
from .evaluate import build

RES = Path(__file__).resolve().parent.parent / "results"

# (case id, item, document condition, expectation)
CASES = [
    *[(f"violation_{i}", i, "headed", "not_cleared") for i in
      ("a9_u2_violation_1", "a10_u4_violation_1", "a12_u1_violation_2", "a14_u1_violation_1", "a15_u5_violation_2")],
    *[(f"compliant_{i}", i, "headed", "not_rejected") for i in
      ("a9_u2_compliant", "a10_u1_compliant", "a12_u3_compliant", "a14_u4_compliant", "a15_u7_compliant")],
    ("injected_authority", "a14_u2_violation_2", "authority", "flagged_not_cleared"),
    ("injected_assurance", "a12_u2_violation_1", "assurance", "flagged_not_cleared"),
    ("plain_violation_a9", "a9_u5_violation_1", "plain", "segmented_not_cleared"),
    ("plain_violation_a10", "a10_u6_violation_1", "plain", "segmented_not_cleared"),
]


def doc_for(it, cond: str) -> str:
    if cond in ("headed", "plain"):
        return build(it, cond)
    return apply(cond, it)[0]  # perturbation of the excerpt itself, headed


def check(case) -> dict:
    cid, iid, cond, expect = case
    it = ITEMS[iid]
    r = screen(doc_for(it, cond), it.system_outline, articles=[it.article])
    v = r["articles"][0]["verdict"]
    caught = v in ("likely non-compliant", "needs human review")  # "no section found" is not a pass
    ok = {"not_cleared": caught,
          "not_rejected": v in ("likely compliant", "needs human review"),
          "flagged_not_cleared": bool(r["flags"]) and caught,
          "segmented_not_cleared": r["segmented"] and caught}[expect]
    return {"case": cid, "expert": f"{sorted(it.human)}", "expect": expect, "verdict": v,
            "flags": len(r["flags"]), "segmented": r["segmented"], "pass": ok}


ITEMS = {}


def main():
    ITEMS.update({it.item_id: it for it in load_items()})
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(check, CASES))
    md = ["# Screener regression suite", "", f"{sum(r['pass'] for r in res)}/{len(res)} cases pass.", "",
          "| case | expert scores | expectation | verdict | flags | segmented | pass |", "|---|---|---|---|---|---|---|"]
    md += [f"| {r['case']} | {r['expert']} | {r['expect']} | {r['verdict']} | {r['flags']} | {r['segmented']} | "
           f"{'yes' if r['pass'] else '**NO**'} |" for r in res]
    (RES / "regression.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    sys.exit(0 if all(r["pass"] for r in res) else 1)


if __name__ == "__main__":
    main()
