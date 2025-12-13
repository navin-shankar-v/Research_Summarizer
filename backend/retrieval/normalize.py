import re

def canonical_title(t: str) -> str:
    t = (t or "").lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

def dedupe(papers):
    seen = set()
    out = []
    for p in papers:
        key = canonical_title(p.get("title", ""))
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def normalize_paper(p):
    """
    Ensures every retrieved paper has the required fields
    for the summarizer prompt.
    """

    title = (p.get("title") or "").strip()
    abstract = (p.get("abstract") or "").strip()

    # authors may be list or str → normalize
    authors = p.get("authors", [])
    if isinstance(authors, list):
        authors = ", ".join([a.strip() for a in authors if a])

    return {
        "title": title or "Untitled",
        "authors": authors or "Unknown",
        "abstract": abstract or "No abstract available.",
        "url": p.get("url", ""),
        "year": p.get("year", "Unknown"),
        "source": p.get("source", "arxiv"),
    }
