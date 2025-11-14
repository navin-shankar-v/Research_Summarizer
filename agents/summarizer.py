import json
import re
import concurrent.futures
from agents._llm import chat_completion

def make_summary(papers):
    """
    Generate a single combined summary for provided papers.
    Includes a 60-second timeout and tolerant JSON parsing.
    """
    numbered = []
    for i, p in enumerate(papers[:10], start=1):
        numbered.append(
            f"[{i}] {p.get('title','').strip()} ({p.get('year','')})\n"
            f"{(p.get('abstract','') or '').strip()}\nURL: {p.get('url','')}"
        )
    context = "\n\n".join(numbered) if numbered else "No papers available."

    messages = [
        {"role": "system", "content": "You are a precise scientific summarizer."},
        {"role": "user", "content": f"""
Summarize the following papers collectively (each labeled [#N]).
Return valid JSON with keys:
- paragraphs: list[str]
- whats_new: list[str]
- open_problems: list[str]
- top5_papers: list[{{"title": str, "url": str}}]
If you cannot return JSON, return plain text.
PAPERS:
{context}
""".strip()},
    ]

    # Run the LLM call in a separate thread with timeout
    try:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            future = ex.submit(chat_completion, messages)
            out = future.result(timeout=360)
        content = out["choices"][0]["message"]["content"]
    except concurrent.futures.TimeoutError:
        return {
            "paragraphs": ["Summary generation timed out."],
            "whats_new": [],
            "open_problems": [],
            "top5_papers": [],
        }
    except Exception as e:
        return {
            "paragraphs": [f"Error during model call: {e}"],
            "whats_new": [],
            "open_problems": [],
            "top5_papers": [],
        }

    # Try parsing JSON output
    try:
        parsed = json.loads(content)
        if isinstance(parsed, list):
            parsed = parsed[0]
        return parsed
    except Exception:
        # Try extracting JSON substring from text
        json_match = re.search(r"\{.*\}", content, re.S)
        if json_match:
            try:
                parsed = json.loads(json_match.group(0))
                return parsed
            except Exception:
                pass

    # Fallback to raw text if nothing else works
    return {
        "paragraphs": [content.strip() or "Summary unavailable."],
        "whats_new": [],
        "open_problems": [],
        "top5_papers": [],
    }
