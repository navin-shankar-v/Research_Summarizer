
import json
from config.settings import settings
from agents._llm import chat_completion

def plan_query(query: str, date_range=None):
    date_hint = date_range.dict() if getattr(date_range, "dict", None) else None
    prompt = f'''
You are a research planning assistant.
User query: "{query}"
Create JSON:
- keywords: 5-8 search terms
- include: 2-4 phrases
- exclude: 0-3 phrases
- date_window: ISO start-end or null (prefer last 3 years)
Date hint: {date_hint}
Return ONLY JSON.
'''.strip()

    out = chat_completion([
        {"role":"system","content":"You are a research planner."},
        {"role":"user","content":prompt}
    ])
    content = out["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except Exception:
        # safe default
        return {"keywords": query.split(), "include": [], "exclude": [], "date_window": None}
