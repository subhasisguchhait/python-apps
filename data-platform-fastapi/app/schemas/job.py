from pydantic import BaseModel
from datetime import datetime

class JobResponse(BaseModel):
    id: int
    dataset_id: int
    status: str
    message: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = {
            "from_attributes": True 
        }