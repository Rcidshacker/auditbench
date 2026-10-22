"""Load AIReg-Bench items and their expert / LLM compliance labels.

AIReg-Bench (Marino et al. 2025, arXiv:2510.01474) ships 120 expert-annotated
technical-documentation excerpts for EU AI Act Articles 9, 10, 12, 14, 15.
Annotation sheets are keyed by (article, scenario label A/B/C, use); the label
is a seeded permutation of (compliant, violation 1, violation 2), recorded in
rand_assign.txt. This module undoes that permutation so every item points at
its documentation file.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent / "external" / "aireg-bench"
ARTICLES = [9, 10, 12, 14, 15]
USES = range(1, 9)  # the 8 intended uses the experts graded
SCENARIOS = ["Scenario A", "Scenario B", "Scenario C"]


@dataclass
class Item:
    item_id: str
    article: int
    use: int
    system: int
    scenario: str  # A/B/C label as annotated
    variant: str  # "compliant" | "violation_1" | "violation_2" (ground truth of generation)
    documentation: str
    system_outline: str
    article_text: str
    human: list[float] = field(default_factory=list)  # one compliance score per annotator

    @property
    def human_median(self) -> float:
        return float(np.nanmedian(self.human))


def _article_texts() -> dict[int, str]:
    txt = (ROOT / "articles.txt").read_text(encoding="utf-8")
    out = {}
    for art in ARTICLES:
        m = re.search(rf"(^\s*\*\*Article\s+{art}\b[\s\S]+?)(?=^\s*\*\*Article\s+\d+\b|\Z)", txt, re.M)
        out[art] = m.group(1).strip()
    return out


def _rand_assign() -> dict[tuple[int, int, int], str]:
    """(use, article, scenario_num) -> 'Scenario X'; 1=compliant, 2/3=violations."""
    mapping, use, art = {}, None, None
    for line in (ROOT / "rand_assign.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if m := re.match(r"Use\s+(\d+),\s*Article\s+(\d+)", line):
            use, art = map(int, m.groups())
        elif m := re.match(r"(\d+)\s*--\s*([ABC])$", line):
            mapping[(use, art, int(m.group(1)))] = f"Scenario {m.group(2)}"
    return mapping


def read_score_sheet(df: pd.DataFrame) -> dict[tuple[int, str, int], float]:
    """Parse one annotation sheet into {(article, scenario, use): compliance score}.

    Layout: row 0 holds 'Use N' over each block, row 1 the sub-headers, rows 2+
    hold 'Art X / Scenario Y' labels in column 0.
    """
    out = {}
    cols = [c for c in range(df.shape[1]) if str(df.iat[1, c]).strip() == "Compliance [1-5]"]
    for c in cols:
        use = int(re.search(r"\d+", str(df.iat[0, c])).group())
        for r in range(2, df.shape[0]):
            label = str(df.iat[r, 0])
            m = re.match(r"Art\s+(\d+)\s*/\s*(Scenario [ABC])", label)
            if not m:
                continue
            v = pd.to_numeric(df.iat[r, c], errors="coerce")
            out[(int(m.group(1)), m.group(2), use)] = float(v)
    return out


def load_items() -> list[Item]:
    arts = _article_texts()
    assign = _rand_assign()
    sheets = pd.read_excel(ROOT / "human_annotations.xlsx", sheet_name=None, header=None)
    humans = [read_score_sheet(df) for df in sheets.values()]

    items = []
    for art in ARTICLES:
        for use in USES:
            system = 1 if use <= 5 else 2  # mirrors LLM_annotation.py: annotators switched system at Use 6
            outline = (ROOT / "system_outlines" / f"Use{use}" / f"System{system}.txt").read_text(encoding="utf-8")
            base = ROOT / "documentation" / f"Article{art}" / f"Use{use}" / f"System{system}"
            for sn, variant, fname in [(1, "compliant", "Compliance.txt"), (2, "violation_1", "Violation_1.txt"),
                                       (3, "violation_2", "Violation_2.txt")]:
                scen = assign[(use, art, sn)]
                items.append(Item(
                    item_id=f"a{art}_u{use}_{variant}",
                    article=art, use=use, system=system, scenario=scen, variant=variant,
                    documentation=(base / fname).read_text(encoding="utf-8"),
                    system_outline=outline, article_text=arts[art],
                    human=[h.get((art, scen, use), np.nan) for h in humans],
                ))
    return items


def load_llm_baseline(model: str, items: list[Item]) -> dict[str, float]:
    """Published AIReg-Bench annotations for a frontier model, keyed by item_id."""
    path = ROOT / "llm_annotations" / f"{model}_annotations.xlsx"
    df = next(iter(pd.read_excel(path, sheet_name=None, header=None).values()))
    scores = read_score_sheet(df)
    return {it.item_id: scores.get((it.article, it.scenario, it.use), np.nan) for it in items}


BASELINE_MODELS = ["gpt5", "o3", "o3_mini", "4o", "sonnet", "pro", "flash", "gemma", "grok3_mini", "grok4"]
