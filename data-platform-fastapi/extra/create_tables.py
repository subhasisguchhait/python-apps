from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    source = Column(String(255), nullable=False)
    format = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    created_at = Column(DateTime , default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)


