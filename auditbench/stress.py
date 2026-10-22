"""Item-level, label-preserving perturbations.

L3 dossier_{first,middle,last}: the target excerpt is embedded among the *compliant* excerpts for the other four
    Articles of the same system and use, which approximates a full Annex IV technical file.
L5 rename: company/product names are swapped for fresh ones, a weak probe for memorised verdicts
    (AIReg-Bench has been public since Oct 2025).

    python -m auditbench.stress --extract-names   # one-off: build results/L5_names.json via diffusiongemma
"""
from __future__ import annotations

import argparse
import json
import re
from functools import cache
from pathlib import Path

from .data import ARTICLES, ROOT, Item, load_items

NAMES = Path(__file__).resolve().parent.parent / "results" / "L5_names.json"


def _compliant_excerpt(article: int, use: int, system: int) -> str:
    return (ROOT / "documentation" / f"Article{article}" / f"Use{use}" / f"System{system}" / "Compliance.txt").read_text(
        encoding="utf-8")


def dossier(item: Item, position: str) -> str:
    others = [_compliant_excerpt(a, item.use, item.system) for a in ARTICLES if a != item.article]
    slot = {"first": 0, "middle": len(others) // 2, "last": len(others)}[position]
    parts = others[:slot] + [item.documentation] + others[slot:]
    return "\n\n---\n\n".join(parts)


# fresh names unlikely to co-occur with AIReg-Bench text; index chosen per original name, so mapping is stable
FRESH_ORGS = ["Halvorsen Analytics", "Quillmark Systems", "Ostrava Applied AI", "Brightwater Labs", "Kestrel Data GmbH",
              "Moravec Solutions", "Tinderbox Intelligence", "Ardent Loop Ltd", "Pelham & Ruiz AI", "Northgate Cognition"]
FRESH_PRODUCTS = ["Atlas-7 Engine", "Verity Core", "Lumen Assess", "Cobalt Sentinel", "Harbor Insight",
                  "Meridia Scan", "Fathom Grade", "Orison Watch", "Tessel Review", "Quarry Signal"]


@cache
def _name_map() -> dict[str, dict[str, str]]:
    return json.loads(NAMES.read_text(encoding="utf-8")) if NAMES.exists() else {}


def rename(item: Item) -> tuple[str, str]:
    names = _name_map().get(item.item_id)
    if names is None:
        raise KeyError(f"no extracted names for {item.item_id}; run `python -m auditbench.stress --extract-names`")
    doc, outline = item.documentation, item.system_outline
    for old, new in sorted(names.items(), key=lambda kv: -len(kv[0])):  # longest first: avoid partial overlaps
        doc = re.sub(re.escape(old), new, doc)
        outline = re.sub(re.escape(old), new, outline)
    return doc, outline


def apply(perturbation: str, item: Item) -> tuple[str, str]:
    if perturbation.startswith("dossier_"):
        return dossier(item, perturbation.split("_", 1)[1]), item.system_outline
    if perturbation == "rename":
        return rename(item)
    raise KeyError(perturbation)


def extract_names():
    """Ask diffusiongemma for the proper names in each document, then assign fresh replacements."""
    from concurrent.futures import ThreadPoolExecutor

    from .openjev import chat

    items = load_items()
    out = _name_map().copy()

    def one(it: Item):
        prompt = ("List every company/organisation name and every product/system/model brand name that appears in "
                  "the text below. Exclude laws, regulators, standards, generic technologies (e.g. 'Transformer', "
                  "'GDPR', 'EU AI Act', 'ISO 27001') and person roles. Answer with a JSON object only: "
                  '{"organisations": [...], "products": [...]}, using the exact spelling from the text.\n\nTEXT:\n'
                  + it.system_outline + "\n\n" + it.documentation)
        txt = chat(prompt, max_tokens=300)["choices"][0]["message"]["content"]
        js = json.loads(re.search(r"\{.*\}", txt, re.S).group())
        mapping = {}
        for kind, pool in (("organisations", FRESH_ORGS), ("products", FRESH_PRODUCTS)):
            for name in js.get(kind, []):
                name = name.strip()
                # only keep names that literally occur, and skip very short tokens that would over-match
                if len(name) >= 4 and (name in it.documentation or name in it.system_outline):
                    mapping[name] = pool[sum(map(ord, name)) % len(pool)]
        return it.item_id, mapping

    todo = [it for it in items if it.item_id not in out]
    with ThreadPoolExecutor(4) as ex:
        for iid, m in ex.map(one, todo):
            out[iid] = m
    NAMES.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    empty = [k for k, v in out.items() if not v]
    print(f"names for {len(out)} items; {len(empty)} with no names found")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract-names", action="store_true")
    if ap.parse_args().extract_names:
        extract_names()
