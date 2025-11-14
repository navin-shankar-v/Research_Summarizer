
from fastapi import FastAPI
from api.routers.summarize import router as summarize_router

app = FastAPI(title="Automated Research Summarization API")
app.include_router(summarize_router, prefix="/api", tags=["summarize"])
