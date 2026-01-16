from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...core.database import get_db
from ...models.job import Job
from ...schemas.job import JobResponse
from ...schemas.processing import process_dataset
from ...api.deps import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/dataset/{dataset_id}", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job_for_dataset(
    dataset_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_job = Job(dataset_id=dataset_id)
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)

    # Start background processing
    background_tasks.add_task(process_dataset, dataset_id, db)


    ## Pydantic v2 compatible way to return the response model
    
    # return JobResponse(
    #     id=new_job.id,
    #     dataset_id=new_job.dataset_id,
    #     status=new_job.status,
    #     message=new_job.message,
    #     created_at=new_job.created_at,
    #     updated_at=new_job.updated_at,
    # )

    # return new_job

    return JobResponse.model_validate(new_job.__dict__)  # Using model_validate for Pydantic v2 compatibility

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobResponse.model_validate(job.__dict__)  # Using model_validate for Pydantic v2 compatibility   
