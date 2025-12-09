# agents/summarizer.py
import json
import re
import concurrent.futures
from agents._llm import chat_completion


def make_summary(papers):
    """
    Generate a deep, structured summary over all papers.
    Returns a dict matching SummaryOut.
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
                "You write deep, technically precise summaries for graduate-level readers."
            ),
        },
        {
            "role": "user",
            "content": f"""
You are given several research papers (each labeled [#N]).

Write a **deep, structured literature summary** across ALL papers.

1. First, write 3–5 dense paragraphs that:
   - synthesize the main ideas,
   - compare methods,
   - highlight trade-offs and trends.

2. Then extract:
   - key_findings: 5–8 technical findings.
   - limitations: 4–6 methodological or conceptual gaps.
   - future_work: 4–6 important next steps.
   - methods: 3–6 study/algorithm patterns.
   - whats_new: 3–5 novel contributions.
   - open_problems: 3–5 unresolved research questions.
   - top5_papers: title + url.

Return **ONLY valid JSON** with this structure:

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

    # Try parsing JSON
    try:
        parsed = json.loads(content)
        if isinstance(parsed, list):
            parsed = parsed[0]
    except:
        match = re.search(r"\{.*\}", content, re.S)
        parsed = json.loads(match.group(0)) if match else {}

    # Safe extraction helper
    def safe_list(key):
        v = parsed.get(key)
        return v if isinstance(v, list) else []

    return {
        "paragraphs": safe_list("paragraphs") or ["Summary unavailable."],
        "key_findings": safe_list("key_findings"),
        "limitations": safe_list("limitations"),
        "future_work": safe_list("future_work"),
        "methods": safe_list("methods"),
        "whats_new": safe_list("whats_new"),
        "open_problems": safe_list("open_problems"),
        "top5_papers": parsed.get("top5_papers") or [],
    }
