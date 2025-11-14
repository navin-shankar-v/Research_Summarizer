
from typing import Dict, List
from retrieval.arxiv_client import search_arxiv
from retrieval.normalize import dedupe

def fetch_papers(plan: Dict, n: int = 8, sources: List[str] = ["arxiv"]):
    q_terms = plan.get("keywords") or []
    query = " ".join(q_terms) if q_terms else plan.get("raw", "")
    papers = []

    if "arxiv" in sources:
        papers += search_arxiv(query, max_results=max(n*2, 12))

    papers = dedupe(papers)
    return papers[:n]
