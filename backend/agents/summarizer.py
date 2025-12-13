# agents/summarizer.py
import json
import re
import concurrent.futures
from agents._llm import chat_completion


def make_summary(papers):
    """
    Generate a deep, structured summary over all papers.
    Returns a dict with guaranteed sections so the frontend never breaks.
    """

    # Build paper context
    numbered = []
    for i, p in enumerate(papers[:10], start=1):
        numbered.append(
            f"[{i}] {p.get('title','').strip()} "
            f"({p.get('year','')})\n"
            f"AUTHORS: {p.get('authors','')}\n"
            f"ABSTRACT: {(p.get('abstract','') or '').strip()}\n"
            f"URL: {p.get('url','')}"
        )

    context = "\n\n".join(numbered) if numbered else "No papers available."

    # LLM prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert scientific reviewer. "
                "You write deep, technically precise summaries."
            ),
        },
        {
            "role": "user",
            "content": f"""
You are given several research papers (each labeled [#N]).

Write a **deep, structured literature summary** across ALL papers.

Return ONLY valid JSON with the structure:

{{
  "paragraphs": [],
  "key_findings": [],
  "limitations": [],
  "future_work": [],
  "methods": [],
  "whats_new": [],
  "open_problems": [],
  "top5_papers": []
}}

PAPERS:
{context}
""".strip(),
        },
    ]

    # LLM call with timeout
    try:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            future = ex.submit(chat_completion, messages)
            out = future.result(timeout=120)
        content = out["choices"][0]["message"]["content"]

    except Exception as e:
        return {
            "paragraphs": [f"Model error: {e}"],
            "key_findings": [],
            "limitations": [],
            "future_work": [],
            "methods": [],
            "whats_new": [],
            "open_problems": [],
            "top5_papers": [],
        }

    # ---------- SAFE JSON RECOVERY ----------
    try:
        parsed = json.loads(content)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except:
                parsed = {}
        else:
            parsed = {}

    # Ensure all sections always exist
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

    clean = {}
    for key, default_val in DEFAULT.items():
        v = parsed.get(key)
        clean[key] = v if isinstance(v, list) else default_val

    return clean
