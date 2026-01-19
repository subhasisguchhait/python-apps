from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime 


class DatasetCreate(BaseModel):
    name: str = Field(..., description="Name of the dataset")
    source: str = Field(..., description="Source of the dataset (e.g., database, API, s3 bucket)")
    format: str = Field(..., description="Format of the dataset (e.g., CSV, JSON)")
    owner: Optional[str] = Field(None, description="Owner of the dataset")


class DatasetResponse(BaseModel):
    id: int = Field(..., description="Unique identifier of the dataset")
    name: str = Field(..., description="Name of the dataset")
    source: str = Field(..., description="Source of the dataset (e.g., database, API, s3 bucket)")
    format: str = Field(..., description="Format of the dataset (e.g., CSV, JSON)")
    owner: Optional[str] = Field(None, description="Owner of the dataset")
    created_at: datetime = Field(..., description="Timestamp when the dataset was created")
    updated_at: datetime = Field(..., description="Timestamp when the dataset was last updated")


class DatasetUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the dataset")
    source: Optional[str] = Field(None, description="Source of the dataset (e.g., database, API, s3 bucket)")
    format: Optional[str] = Field(None, description="Format of the dataset (e.g., CSV, JSON)")
    owner: Optional[str] = Field(None, description="Owner of the dataset")

class DatasetMultipleUpdate(BaseModel):
    id: int = Field(..., description="Unique identifier of the dataset")
    name: Optional[str] = Field(None, description="Name of the dataset")
    source: Optional[str] = Field(None, description="Source of the dataset (e.g., database, API, s3 bucket)")
    format: Optional[str] = Field(None, description="Format of the dataset (e.g., CSV, JSON)")
    owner: Optional[str] = Field(None, description="Owner of the dataset")
