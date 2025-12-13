# agents/summarizer.py
import json
import re
import concurrent.futures
from agents._llm import chat_completion


# -----------------------------------------------------------
# SAFE JSON HELPERS
# -----------------------------------------------------------

def safe_json_extract(text: str):
    """Extract JSON object safely from LLM output."""
    try:
        return json.loads(text)
    except:
        pass

    # Try regex recovery
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return {}

    return {}


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


def normalize_output(parsed):
    """Ensure all keys exist and are of correct type."""
    clean = {}
    for key, default_val in DEFAULT.items():
        val = parsed.get(key)
        clean[key] = val if isinstance(val, list) else default_val
    return clean


# -----------------------------------------------------------
# MAIN SUMMARY FUNCTION
# -----------------------------------------------------------

def make_summary(papers):
    """
    Generate deep structured summary over the retrieved papers.
    ALWAYS returns complete dict → frontend never breaks.
    """

    # Build multi-paper context
    chunks = []
    for i, p in enumerate(papers[:10], start=1):
        chunks.append(
            f"[{i}] {p.get('title','Untitled')} ({p.get('year','')})\n"
            f"AUTHORS: {p.get('authors','N/A')}\n"
            f"ABSTRACT: {(p.get('abstract','') or '').strip()}\n"
            f"URL: {p.get('url','')}"
        )
    context = "\n\n".join(chunks) if chunks else "No papers found."

    # LLM Prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert scientific reviewer. "
                "Produce deep, accurate, multi-paper literature summaries. "
                "ABSOLUTELY NO TEXT OUTSIDE JSON."
            )
        },
        {
            "role": "user",
            "content": f"""
Summarize ALL papers provided. Produce a structured literature review.

Return ONLY valid JSON:

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

Rules:
- Write 2–4 paragraphs (technical, dense, coherent).
- Extract REAL findings from the abstracts.
- Do NOT hallucinate unavailable information.
- Leave sections empty if papers do not mention them.
- For top5_papers: return objects like:
    {{ "title": "...", "url": "..." }}

PAPERS:
{context}
""".strip()
        }
    ]

    # Execute with timeout
    try:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            future = ex.submit(chat_completion, messages)
            response = future.result(timeout=120)
        raw = response["choices"][0]["message"]["content"]

    except Exception as e:
        return normalize_output({"paragraphs": [f"Model error: {e}"]})

    # Parse JSON safely
    parsed = safe_json_extract(raw)
    return normalize_output(parsed)
