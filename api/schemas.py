
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DateRange(BaseModel):
    start: Optional[str] = None  # YYYY-MM-DD
    end: Optional[str] = None

class SummarizeReq(BaseModel):
    query: str = Field(..., min_length=3)
    n_papers: int = 8
    date_range: Optional[DateRange] = None
    sources: List[str] = ["arxiv"]

class Paper(BaseModel):
    title: str
    authors: List[str]
    year: int | None = None
    abstract: str
    url: str
    source: str

class SummaryOut(BaseModel):
    paragraphs: List[str]
    whats_new: List[str]
    open_problems: List[str]
    top5_papers: List[Dict[str, str]]

class EvalOut(BaseModel):
    rougeL: float | None = None
    bertscore_f1: float | None = None
    citation_grounding: float | None = None

class SummarizeResp(BaseModel):
    plan: Dict
    papers: List[Paper]
    summary: SummaryOut
    eval: EvalOut | None = None
