"""Voiceover script. Each line: (name, segment, offset seconds into that segment, slot seconds, text).

Segments match video/edit.py: intro (30 s of title cards), land, dossier, inject, results, find, outro.
Results render about 18 s into the dossier clip and 20 s into the injected clip, so lines are split around that.
"""

LINES = [
    ("n01", "intro", 0.5, 7.0, "This is AuditBench Screener: EU AI Act pre-screening, built on NVIDIA Nemotron and Nebius."),
    ("n02", "intro", 8.4, 10.2, "From December 2027, high-risk AI must document compliance with Articles 9 to 15. "
                               "Reviewers will lean on language models to check it."),
    ("n03", "intro", 19.4, 10.2, "We tested those models on 120 expert-labelled files. Hide a violation early in a long "
                                "file, and they miss up to 37 percent."),
    ("n04", "land", 0.6, 16.5, "So we built a screener. You paste a technical file and get a verdict for each Article. "
                               "Every design choice answers a failure we measured in the research."),
    ("n05", "dossier", 0.5, 17.3, "Here is a full five-section technical file. The Article 14 section quietly hides a "
                                  "human-oversight gap. Each Article is judged on its own, by three Nemotron Nano samples "
                                  "on Nebius Token Factory. Disagreements go to Nemotron Ultra."),
    ("n06", "dossier", 18.5, 11.3, "Article 14 comes back likely non-compliant, while the compliant sections pass. Every "
                                   "quote shown is checked against the source text."),
    ("n07", "inject", 0.5, 18.5, "This file adds a note telling the reviewer it was pre-approved by the EU AI Office. A "
                                 "careless judge might take the hint."),
    ("n08", "inject", 20.0, 9.6, "The Screener flags the note, ignores it as evidence, and still finds the real gaps."),
    ("n09", "results", 0.3, 10.4, "Across all 120 files, a whole-file judge missed 37 percent of violations. The Screener "
                                 "missed 5.5."),
    ("n10", "find", 0.4, 13.2, "Fake approvals cleared nothing, and a rewrite attack worked once in 32. Close calls go "
                               "to a human, on purpose."),
    ("n11", "outro", 0.4, 7.6, "AuditBench Screener. Open source, and live today."),
]
