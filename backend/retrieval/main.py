from .arxiv_client import search_arxiv
from .normalize import normalize_paper, dedupe


def retrieve_papers(query: str, n: int = 5):
    # get raw papers
    raw = search_arxiv(query, max_results=n)

    # normalize each
    clean = [normalize_paper(p) for p in raw]

    # remove duplicates
    clean = dedupe(clean)

    return clean
