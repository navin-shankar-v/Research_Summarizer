
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

ARXIV_API = "http://export.arxiv.org/api/query"

def search_arxiv(query: str, max_results=12, start=0, categories=("cs.LG","cs.AI")):
    if not query:
        query = "machine learning"
    q = f'all:"{query}"'
    if categories:
        cats = " OR ".join([f"cat:{c}" for c in categories])
        q = f"({q}) AND ({cats})"
    params = {
        "search_query": q,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    try:
        r = requests.get(ARXIV_API, params=params, timeout=20)
        r.raise_for_status()
        return parse_arxiv_atom(r.text)
    except Exception:
        # Offline fallback minimal mock
        return [{
            "title": "Mock arXiv Paper",
            "authors": ["Author A"],
            "year": 2024,
            "abstract": "Mock abstract when offline.",
            "url": "http://arxiv.org/abs/0000.00000",
            "source": "arxiv"
        }]

def parse_arxiv_atom(atom_xml: str):
    ns = {"a":"http://www.w3.org/2005/Atom"}
    root = ET.fromstring(atom_xml)
    results = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip().replace("\n"," ")
        abstract = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
        link = ""
        for l in entry.findall("a:link", ns):
            if l.attrib.get("type") == "text/html":
                link = l.attrib.get("href","")
        authors = [a.findtext("a:name", default="", namespaces=ns) for a in entry.findall("a:author", ns)]
        pub = entry.findtext("a:published", default="", namespaces=ns)
        year = None
        if pub:
            try:
                year = datetime.fromisoformat(pub.replace("Z","")).year
            except Exception:
                pass
        results.append({
            "title": title, "authors": authors, "year": year,
            "abstract": abstract, "url": link or "",
            "source": "arxiv"
        })
    return results
