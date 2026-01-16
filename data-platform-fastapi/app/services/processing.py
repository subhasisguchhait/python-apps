import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.job import Job


async def process_dataset(dataset_id: int, db: AsyncSession) :
    try:
        result = await db.execute(select(Job).where(Job.dataset_id == dataset_id))
        job  = result.scalar_one()
        job.status = "RUNNING"
        await db.commit()

        # Simulate some processing time
        await asyncio.sleep(5)  # Simulate processing delay

        # Update job status to COMPLETED
        job.status = "COMPLETED"
        job.message = "Processing finished successfully."
        await db.commit()
    except Exception as e:
        job.status = "FAILED"
        job.message = f"Processing failed: {str(e)}"
        await db.commit()
    
