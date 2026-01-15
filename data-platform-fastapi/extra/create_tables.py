from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
import os



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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime , default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))   

if __name__ == "__main__":
    print("CWD:", os.getcwd())
    print("Engine URL:", engine.url)
    print("Absolute DB path exists:", os.path.exists(os.path.abspath("./app.db")))

    # creates missing tables only
    Base.metadata.create_all(bind=engine)

    # # or create a single table explicitly (checkfirst=True prevents recreate)
    # Dataset.__table__.create(bind=engine, checkfirst=True)
    # User.__table__.create(bind=engine, checkfirst=True)
    # print("Tables created successfully.")

    # show tables
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        print("Existing tables in the database:")
        for table in tables:
            print(table[0]) 


