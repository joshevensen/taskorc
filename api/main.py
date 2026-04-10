import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routers.artifact import router as artifact_router
from app.routers.auth import router as auth_router
from app.routers.log import router as log_router
from app.routers.note import router as note_router
from app.routers.project import router as project_router
from app.routers.task import router as task_router
from app.routers.user import router as user_router

logger = logging.getLogger(__name__)

app = FastAPI(title="TaskOrc API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(note_router)
app.include_router(log_router)
app.include_router(artifact_router)


@app.get("/health")
def health():
    return {"status": "ok"}
