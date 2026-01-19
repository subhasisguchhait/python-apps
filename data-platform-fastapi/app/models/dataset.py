from ..core.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    source = Column(String(255), nullable=False)
    format = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    created_at = Column(DateTime , default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
