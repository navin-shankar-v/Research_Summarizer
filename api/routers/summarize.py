
from fastapi import APIRouter, HTTPException
from api.schemas import SummarizeReq, SummarizeResp
from agents.planner import plan_query
from agents.retriever import fetch_papers
from agents.summarizer import make_summary
from agents.evaluator import evaluate_summary

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResp)
def summarize(req: SummarizeReq):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    plan = plan_query(req.query, req.date_range)
    papers = fetch_papers(plan, n=req.n_papers, sources=req.sources)
    summary = make_summary(papers)
    scores = evaluate_summary(summary, papers)

    return {"plan": plan, "papers": papers, "summary": summary, "eval": scores}
