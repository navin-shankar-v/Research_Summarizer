# agents/tracking.py
import json
from typing import Dict, List

import mlflow
from config.settings import settings

# local file-based tracking
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("auto-research-summarizer")


def log_summarization_run(
    req: Dict,
    plan: Dict,
    papers: List[Dict],
    summary: Dict,
    eval_scores: Dict,
    latency_s: float,
) -> None:
    """
    Logs one summarization run to MLflow.
    """
    with mlflow.start_run(run_name=req.get("query", "")[:50]):
        # params
        mlflow.log_param("query", req.get("query"))
        mlflow.log_param("n_papers", req.get("n_papers"))
        mlflow.log_param("sources", ",".join(req.get("sources", [])))
        mlflow.log_param("llm_provider", settings.llm_provider)
        mlflow.log_param("model", getattr(settings, "openai_model", None) or getattr(settings, "ollama_model", None))

        # metrics
        for k, v in (eval_scores or {}).items():
            try:
                mlflow.log_metric(k, float(v))
            except Exception:
                pass
        mlflow.log_metric("latency_s", float(latency_s))
        mlflow.log_metric("num_papers", len(papers))
        mlflow.log_metric("num_paragraphs", len(summary.get("paragraphs", [])))

        # artifacts (JSON blobs)
        mlflow.log_text(json.dumps(plan, indent=2), "plan.json")
        mlflow.log_text(json.dumps(papers, indent=2), "papers.json")
        mlflow.log_text(json.dumps(summary, indent=2), "summary.json")
        mlflow.log_text(json.dumps(eval_scores, indent=2), "eval_scores.json")
