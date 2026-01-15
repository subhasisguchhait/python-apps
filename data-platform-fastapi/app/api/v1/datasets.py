from fastapi import HTTPException, status, APIRouter, Depends, Query
from ...schemas.dataset import DatasetCreate, DatasetResponse, DatasetUpdate, DatasetMultipleUpdate
from sqlalchemy import select
from ..core.database import get_db
from ...models.dataset import Dataset
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/datasets", tags=["datasets"])

# @router.post("/create", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
# def create_dataset(dataset: DatasetCreate):
#     """
#     Create a new dataset entry.
#     """
#     # Here you would typically add logic to save the dataset to a database
#     # For demonstration, we will return a mock response
#     new_dataset = DatasetResponse(
#         id=1,
#         name=dataset.name,
#         source=dataset.source,
#         format=dataset.format,
#         owner=dataset.owner,
#         created_at="2024-01-01T00:00:00Z",
#         updated_at="2024-01-01T00:00:00Z"
#     )
#     return new_dataset


@router.post("/create", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(dataset: DatasetCreate, db: AsyncSession = Depends(get_db)):
    db_dataset = Dataset(**dataset.model_dump())
    db.add(db_dataset)
    await db.commit()
    await db.refresh(db_dataset)
    return db_dataset

@router.get("/list/all", response_model=list[DatasetResponse])
async def list_datasets(skip: int = Query(default=0, gte=0), 
                        limit: int = Query(default=10, lte=100),
    db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dataset).offset(skip).limit(limit))
    datasets = result.scalars().all()
    return datasets

@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    return dataset


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(dataset_id: int, updated_data: DatasetUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(dataset, key, value)
    await db.commit()
    await db.refresh(dataset)
    return dataset


@router.delete("/{dataset_id}", status_code=status.HTTP_200_OK)
async def delete_dataset(dataset_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    await db.delete(dataset)
    await db.commit()
    return {"msg": "Dataset deleted successfully"}


@router.put("/update/multiple", response_model=list[DatasetResponse])
async def update_multiple_datasets(datasets: list[DatasetMultipleUpdate], db: AsyncSession = Depends(get_db)):
    updated_datasets = []
    for data in datasets:
        result = await db.execute(select(Dataset).where(Dataset.id == data.id))
        dataset = result.scalar_one_or_none()
        if dataset:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(dataset, key, value)
            updated_datasets.append(dataset)
    await db.commit()
    for dataset in updated_datasets:
        await db.refresh(dataset)
    return updated_datasets

@router.delete("/delete/multiple", status_code=status.HTTP_200_OK)
async def delete_multiple_datasets(dataset_ids: list[int] = Query(...), db: AsyncSession = Depends(get_db)):
    for dataset_id in dataset_ids:
        result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
        dataset = result.scalar_one_or_none()
        if dataset:
            await db.delete(dataset)
    await db.commit()
    return {"msg": "Datasets deleted successfully"} 