# backend/retrieval/main.py

from .arxiv_client import search_arxiv
from .normalize import dedupe

def retrieve_papers(query: str, n: int):
    results = search_arxiv(query, max_results=n)
    results = dedupe(results)
    return results
