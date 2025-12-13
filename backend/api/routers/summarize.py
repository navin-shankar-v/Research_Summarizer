from fastapi import APIRouter
from pydantic import BaseModel
from agents.summarizer import make_summary
from agents.evaluator import evaluate_summary
import logging, json

router = APIRouter()

class Query(BaseModel):
    query: str
    n_papers: int = 5
    sources: list = ["arxiv"]

@router.post("/summarize")
def summarize(q: Query):
    logging.basicConfig(level=logging.INFO)

    # TEMP MARKER
    logging.info("=== /summarize endpoint called ===")

    # Retrieve papers (your existing retrieval pipeline)
    from retrieval.main import retrieve_papers
    papers = retrieve_papers(q.query, q.n_papers)

    logging.info("PAPERS RETRIEVED: " + str(len(papers)))

    summary = make_summary(papers)

    logging.info("SUMMARY RAW:")
    logging.info(json.dumps(summary, indent=2))

    eval_scores = evaluate_summary(summary, papers)

    logging.info("EVAL RAW:")
    logging.info(json.dumps(eval_scores, indent=2))

    return {
        "summary": summary,
        "eval": eval_scores,
        "papers": papers,
    }
