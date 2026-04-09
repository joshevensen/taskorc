from fastapi import FastAPI

from app.core.config import settings
from app.routers.auth import router as auth_router

app = FastAPI(title="TaskOrc API", version="0.1.0")

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}
