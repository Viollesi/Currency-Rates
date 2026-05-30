"""Database connection setup."""

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


@lru_cache
def get_engine() -> Engine:
    """Create SQLAlchemy engine."""
    return create_engine(settings.database_url)


def create_session() -> Session:
    """Create database session."""
    session_factory = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return session_factory()


def get_session() -> Generator[Session, None, None]:
    """Create database session for FastAPI dependencies."""
    session = create_session()
    try:
        yield session
    finally:
        session.close()
