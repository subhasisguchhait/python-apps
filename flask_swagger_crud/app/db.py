# app/db.py - Engine + Session factory + request lifecycle hooks
from __future__ import annotations

from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def init_engine(database_url: str):
    """Create the SQLAlchemy Engine (connection pool) once per app process."""
    return create_engine(
        database_url,
        pool_pre_ping=True,  # Checks dead/stale connections before using them
        future=True,
    )


def init_session_factory(engine):
    """Create a Session factory bound to the engine."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def register_session_handlers(app):
    """
    Create one DB session per request and always close it.
    - On exceptions: rollback so the connection returns to pool cleanly.
    - Always: close session (returns connection to pool).
    """

    @app.before_request
    def open_session():
        g.db = app.SessionLocal()  # request-scoped session stored in Flask's `g`

    @app.teardown_request
    def close_session(exc):
        db: Session | None = getattr(g, "db", None)
        if db is None:
            return
        try:
            if exc is not None:
                db.rollback()  # undo partial work if request failed
        finally:
            db.close()  # always return connection to pool
