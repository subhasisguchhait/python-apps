from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.datasets import router as datasets_router
from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.health import router as health_router
from app.core.logging import setup_logging
from app.middleware.request_logging import log_requests
from app.core.database import engine

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: optional (run migrations, warm caches, etc.)
    yield
    # shutdown: close db pool
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.middleware("http")(log_requests)

app.include_router(datasets_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Async API is running!"}