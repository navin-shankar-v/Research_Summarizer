
# Automated Research Summarization

An AI-powered multi-agent system that plans a search, retrieves papers (arXiv), summarizes findings, and evaluates the output.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp config/settings.example.env .env
# fill OPENAI_API_KEY inside .env
uvicorn api.main:app --reload --port 8000
```

Test:
```bash
python scripts/smoke_run.py
```

Optional UI:
```bash
streamlit run ui/app.py
```

## Environment

See `config/settings.example.env`. If `OPENAI_API_KEY` is not set, the app falls back to a mock LLM response so you can test end‑to‑end without external calls.
