
import re

def canonical_title(t: str) -> str:
    t = (t or "").lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

def dedupe(papers):
    seen = set()
    out = []
    for p in papers:
        key = canonical_title(p.get("title",""))
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out
