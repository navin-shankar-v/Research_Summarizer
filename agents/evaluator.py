# agents/evaluator.py
import math
from typing import Dict, List


def _summary_text(summary: Dict) -> str:
    parts = []
    for p in summary.get("paragraphs", []):
        parts.append(p)
    for sec in ("key_findings", "limitations", "future_work", "methods", "whats_new", "open_problems"):
        vals = summary.get(sec) or []
        if isinstance(vals, list):
            parts.extend(vals)
    return " ".join(parts).lower()


def _token_count(text: str) -> int:
    return len(text.split())


def evaluate_summary(summary: Dict, papers: List[Dict]) -> Dict[str, float]:
    """
    Simple, interpretable evaluation metrics for a summary.

    - coverage: fraction of papers whose title tokens appear in the summary
    - depth: scaled length of the paragraphs
    - structure: how many structured sections are non-empty
    - overall: weighted combination
    """
    text = _summary_text(summary)

    # 1) coverage
    if papers:
        hits = 0
        for p in papers:
            title = (p.get("title") or "").lower()
            tokens = [t for t in title.split() if len(t) > 4][:2]
            if tokens and all(tok in text for tok in tokens):
                hits += 1
        coverage = hits / len(papers)
    else:
        coverage = 0.0

    # 2) depth (based on number of tokens in main paragraphs)
    par_text = " ".join(summary.get("paragraphs", []))
    par_tokens = _token_count(par_text)
    # normalize with a log curve; ~800 tokens ~ 1.0
    depth = min(1.0, math.log1p(par_tokens) / math.log1p(800))

    # 3) structure (how many sections filled)
    sections = ["key_findings", "limitations", "future_work", "methods", "whats_new", "open_problems"]
    filled = 0
    for s in sections:
        val = summary.get(s)
        if isinstance(val, list) and len(val) > 0:
            filled += 1
    structure = filled / len(sections) if sections else 0.0

    overall = 0.4 * coverage + 0.3 * depth + 0.3 * structure

    return {
        "coverage": round(coverage, 3),
        "depth": round(depth, 3),
        "structure": round(structure, 3),
        "overall": round(overall, 3),
    }
