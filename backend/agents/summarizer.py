# agents/summarizer.py
import json
import re
import concurrent.futures
from agents._llm import chat_completion

DEFAULT = {
    "paragraphs": ["Summary unavailable."],
    "key_findings": [],
    "limitations": [],
    "future_work": [],
    "methods": [],
    "whats_new": [],
    "open_problems": [],
    "top5_papers": [],
}

def safe_load_json(text: str):
    """Attempts multiple parses until valid JSON is extracted."""
    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return {}

    return {}

def ensure_structure(parsed: dict):
    """Guarantee all required fields exist and are lists."""
    clean = {}
    for k, default in DEFAULT.items():
        v = parsed.get(k)
        clean[k] = v if isinstance(v, list) else default
    return clean


def build_rag_context(papers):
    """Create a compact digest of each paper (RAG-style context)."""
    chunks = []
    for i, p in enumerate(papers):
        abstract = p.get("abstract", "").strip()
        title = p.get("title", "").strip()
        year = p.get("year", "")

        # Mini-embedding style compression
        chunk = f"""
[Paper {i+1}]
TITLE: {title}
YEAR: {year}
ABSTRACT SUMMARY: {abstract[:600]}...
KEYWORDS: {", ".join(p.get("keywords", [])) if p.get("keywords") else ""}
"""
        chunks.append(chunk)

    return "\n".join(chunks)


def make_summary(papers):
    """Generate structured JSON summary with strong fallback."""
    
    if not papers:
        return DEFAULT

    rag_context = build_rag_context(papers)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert scientific reviewer. "
                "You must output ONLY valid JSON following the exact schema. "
                "No explanations. No prose outside JSON."
            ),
        },
        {
            "role": "user",
            "content": f"""
You are given processed paper digests:

{rag_context}

Write a **deep structured literature review across ALL papers**.

Follow this schema EXACTLY:

{{
  "paragraphs": ["..."],
  "key_findings": ["..."],
  "limitations": ["..."],
  "future_work": ["..."],
  "methods": ["..."],
  "whats_new": ["..."],
  "open_problems": ["..."],
  "top5_papers": [
      {{ "title": "...", "url": "..." }}
  ]
}}

RULES:
- OUTPUT ONLY JSON.
- NO text outside the JSON object.
- Never return empty arrays. If unknown, infer best possible from abstracts.
""",
        },
    ]

    try:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            future = ex.submit(chat_completion, messages)
            out = future.result(timeout=120)

        content = out["choices"][0]["message"]["content"]

    except Exception as e:
        return DEFAULT

    # --- JSON PARSE ---
    parsed = safe_load_json(content)

    # --- Backend ALWAYS returns structured output ---
    cleaned = ensure_structure(parsed)

    return cleaned
