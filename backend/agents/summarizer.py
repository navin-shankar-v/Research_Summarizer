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
            "You are an expert literature review synthesizer trained to produce "
            "structured meta-analysis across multiple papers. "
            "Your output MUST be valid JSON. No explanations."
        ),
    },
    {
        "role": "user",
        "content": f"""
You are given multiple research papers (labeled [#N]).

Produce a **deep, structured literature review** across ALL papers.

Your response MUST follow this exact JSON structure:

{{
  "paragraphs": ["3–5 deep synthesis paragraphs"],
  "key_findings": ["5–8 items"],
  "limitations": ["4–6 items"],
  "future_work": ["4–6 items"],
  "methods": ["3–6 items"],
  "whats_new": ["3–5 innovations"],
  "open_problems": ["3–5 research gaps"],
  "top5_papers": [
        {{"title": "...", "url": "..."}}
  ]
}}

RULES:
- ALWAYS return valid JSON.
- NEVER add extra commentary.
- NEVER escape JSON inside a string.
- Do not include markdown.
- If unsure, produce your best scientific estimate.

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
    except:
        # fallback recovery for malformed JSON
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except:
                parsed = {}
        else:
            parsed = {}

    # enforce defaults so UI never breaks
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

    for k, v in DEFAULT.items():
        if k not in parsed or not isinstance(parsed[k], list):
            parsed[k] = v

