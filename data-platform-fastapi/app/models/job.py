from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone, timedelta
from ..core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, index=True)
    status = Column(String, default="PENDING")  # Possible values: PENDING, RUNNING, COMPLETED, FAILED
    message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))