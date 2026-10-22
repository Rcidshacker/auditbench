"""Run auditor configurations over AIReg-Bench; results are appended to a JSONL cache.

    python -m auditbench.run --configs holistic decomposed --perturbations none assurance --k 3
Re-running skips (config, perturbation, item, sample) rows already in the cache.
"""
from __future__ import annotations

import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .auditors import PERTURBATIONS, build, generative_prompt, parse_generative, score
from .data import load_items
from .openjev import chat, systemone
from .providers import generate

OUT = Path(__file__).resolve().parent.parent / "results" / "runs.jsonl"
CONFIGS = ["holistic", "holistic_noarticle", "holistic_nooutline", "decomposed", "generative"]


def done_keys() -> set[tuple]:
    if not OUT.exists():
        return set()
    return {(r["config"], r["perturbation"], r["item_id"], r["sample"])
            for r in map(json.loads, OUT.read_text(encoding="utf-8").splitlines())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", nargs="+", default=["holistic"],
                    help=f"{CONFIGS} or gen:<provider>:<model> (see providers.py)")
    ap.add_argument("--perturbations", nargs="+", default=["none"], choices=list(PERTURBATIONS) + ["rename", "dossier_first", "dossier_middle", "dossier_last"])
    ap.add_argument("--k", type=int, default=3, help="independent samples per cell (samples=1 each)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=None, help="results file name; use a separate file per concurrent run")
    a = ap.parse_args()
    global OUT
    if a.out:
        OUT = OUT.with_name(a.out)

    items = load_items()[: a.limit]
    seen = done_keys()
    jobs = [(c, p, it, s) for c in a.configs for p in a.perturbations for it in items for s in range(a.k)
            if (c, p, it.item_id, s) not in seen]
    print(f"{len(jobs)} calls to make ({len(seen)} cached)")
    OUT.parent.mkdir(exist_ok=True)
    lock, n_tok, fails = threading.Lock(), 0, 0

    def call(job):
        c, p, it, s = job
        if c == "generative":
            r = chat(generative_prompt(it, p))
            return {"config": c, "perturbation": p, "item_id": it.item_id, "sample": s, "model": r["model"],
                    "input_tokens": r["usage"]["prompt_tokens"],
                    **parse_generative(r["choices"][0]["message"]["content"])}
        if c.startswith("gen:"):  # gen:<provider>:<model>, same AIReg-Bench prompt through another provider
            text, model, ntok = generate(c[4:], generative_prompt(it, p))
            return {"config": c, "perturbation": p, "item_id": it.item_id, "sample": s, "model": model,
                    "input_tokens": ntok, **parse_generative(text)}
        state, qs = build(c, it, p)
        r = systemone(state, qs, samples=1)
        return {"config": c, "perturbation": p, "item_id": it.item_id, "sample": s,
                "model": r["model"], "input_tokens": r["usage"]["input_tokens"], **score(c, r["answers"])}

    with ThreadPoolExecutor(a.workers) as ex, OUT.open("a", encoding="utf-8") as f:
        futs = [ex.submit(call, j) for j in jobs]
        for i, fut in enumerate(as_completed(futs), 1):
            try:
                row = fut.result()
            except Exception as e:  # keep going; failures are retried on the next run
                fails += 1
                print("FAIL", e)
                continue
            with lock:
                f.write(json.dumps(row) + "\n")
                n_tok += row["input_tokens"]
            if i % 200 == 0:
                f.flush()
                print(f"{i}/{len(jobs)}  tokens so far {n_tok:,}")
    print(f"done. failures={fails} input_tokens={n_tok:,}")


if __name__ == "__main__":
    main()
