from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title="TaskOrc API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}
