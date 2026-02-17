# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    Maps to DBA-managed table `users`.
    IMPORTANT: table must already exist in the database. Make sure your model matches the table definition (columns, types, constraints).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
