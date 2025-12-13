# agents/evaluator.py

import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """Basic text normalization."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_coverage(summary_text, references):
    """
    Uses TF-IDF + cosine similarity to measure how well
    the summary covers the abstracts of the papers.
    """
    if not references:
        return 0.0

    docs = [summary_text] + references
    docs = [clean_text(d) for d in docs]

    try:
        vec = TfidfVectorizer().fit_transform(docs)
        similarities = cosine_similarity(vec[0:1], vec[1:])[0]
        return float(np.mean(similarities))
    except:
        return 0.0


def compute_depth(summary_text):
    """
    Measures detail level based on:
    - Average sentence length
    - Keyword richness
    """

    sentences = re.split(r"[.!?]+", summary_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0.0

    avg_sentence_len = np.mean([len(s.split()) for s in sentences])
    keyword_count = len(re.findall(r"\b(method|result|analysis|study|data|experiment|model)\b", summary_text.lower()))

    # Normalize heuristically
    sentence_score = min(avg_sentence_len / 20, 1.0)
    keyword_score = min(keyword_count / 10, 1.0)

    return float((sentence_score + keyword_score) / 2)


def compute_structure(summary):
    """
    Checks if required sections exist.
    """
    sections = [
        "key_findings",
        "limitations",
        "future_work",
        "methods",
        "whats_new",
        "open_problems"
    ]
    count = sum(len(summary.get(s, [])) > 0 for s in sections)
    return count / len(sections)


def evaluate_summary(summary, papers):
    """
    CPU-friendly evaluation with NO rouge-score and NO bert-score.
    """

    summary_text = " ".join(summary.get("paragraphs", []))
    if not summary_text.strip():
        return {
            "coverage": 0,
            "depth": 0,
            "structure": 0,
            "overall": 0
        }

    references = [p.get("abstract", "") for p in papers if p.get("abstract")]

    # Compute metrics
    coverage = compute_coverage(summary_text, references)
    depth = compute_depth(summary_text)
    structure = compute_structure(summary)

    overall = (
        0.4 * coverage +
        0.3 * depth +
        0.3 * structure
    )

    return {
        "coverage": round(coverage, 3),
        "depth": round(depth, 3),
        "structure": round(structure, 3),
        "overall": round(overall, 3)
    }
