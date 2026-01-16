from fastapi import FastAPI
from app.api.v1.datasets import router as datasets_router
from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router


app = FastAPI()

app.include_router(datasets_router, prefix="/api/v1") 
app.include_router(auth_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Async API is running!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


