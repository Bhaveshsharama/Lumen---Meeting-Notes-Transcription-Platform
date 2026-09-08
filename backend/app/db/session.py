"""
db/session.py — SQLAlchemy engine, session factory, and DB dependency for FastAPI.

Key design decisions:
- PRAGMA foreign_keys=ON: SQLite disables FK enforcement by default, so cascading
  deletes (meeting → segments, summary, topics, action_items) would silently fail.
  The event listener below turns it on for every connection.
- get_db(): FastAPI Depends() generator that yields a session and guarantees cleanup.
  This is the single point where sessions are created — services and repositories
  never create their own (DIP — they receive the session via constructor injection).
- create_tables(): called once at startup to auto-create all tables from the ORM models.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.db.config import settings
from app.models.base import Base


# ---------- Engine ----------
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite + FastAPI threads
    echo=False,
)


# ---------- SQLite FK enforcement ----------
# Without this, ON DELETE CASCADE / SET NULL in the schema is silently ignored.
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key constraint enforcement for every SQLite connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# ---------- Session factory ----------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------- FastAPI dependency ----------
def get_db() -> Generator[Session, None, None]:
    """
    Yield a database session for the duration of a single request.
    Ensures the session is closed even if the request handler raises.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Table creation ----------
def create_tables() -> None:
    """Create all tables defined by SQLAlchemy models (idempotent)."""
    # Import all models so Base.metadata knows about them
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
