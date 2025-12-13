# agents/evaluator.py

import numpy as np
from rouge_score import rouge_scorer
from bert_score import score as bert_score

def evaluate_summary(summary, papers):
    """
    Computes:
    - ROUGE-1
    - ROUGE-L
    - BERTScore (F1)
    Produces normalized metrics for UI.
    """

    # Combine model-generated paragraphs into text
    summary_text = " ".join(summary.get("paragraphs", []))
    if not summary_text.strip():
        return {"overall": 0, "coverage": 0, "depth": 0, "structure": 0}

    # Use abstracts as references
    references = [
        p.get("abstract", "") for p in papers
        if p.get("abstract")
    ]

    if not references:
        references = [""]  # avoid errors

    # ------------------ ROUGE ------------------
    scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)
    rouge1_scores, rougeL_scores = [], []

    for ref in references:
        r = scorer.score(ref, summary_text)
        rouge1_scores.append(r["rouge1"].fmeasure)
        rougeL_scores.append(r["rougeL"].fmeasure)

    rouge1 = float(np.mean(rouge1_scores))
    rougeL = float(np.mean(rougeL_scores))

    # ------------------ BERTScore ------------------
    try:
        _, _, F1 = bert_score(
            [summary_text] * len(references),
            references,
            lang="en",
            verbose=False
        )
        bert_f1 = float(F1.mean())
    except Exception:
        bert_f1 = 0.0

    # ------------------ Structure Completeness ------------------
    sections = ["key_findings", "limitations", "future_work", "methods", "whats_new", "open_problems"]
    structure = sum(len(summary.get(s, [])) > 0 for s in sections) / len(sections)

    # ------------------ Overall ------------------
    overall = (
        0.35 * rouge1 +
        0.35 * bert_f1 +
        0.30 * structure
    )

    return {
        "coverage": round(rouge1, 3),
        "depth": round(bert_f1, 3),
        "structure": round(structure, 3),
        "overall": round(overall, 3),
    }
